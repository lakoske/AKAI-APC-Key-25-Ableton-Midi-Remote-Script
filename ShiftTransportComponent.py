from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.Control import ButtonControl
from _Framework.TransportComponent import TransportComponent as TransportComponentBase
from _Framework.SubjectSlot import subject_slot
from _Framework.ComboElement import ComboElement
from _Framework.ButtonElement import ButtonElement
from .button_combine import ButtonCombine

class ShiftTransportComponent(TransportComponentBase):
    u""" TransportComponent that only uses certain buttons if a shift button is pressed """
    rec_quantization_button = ButtonControl()

    def __init__(self, *a, **k):
        super(ShiftTransportComponent, self).__init__(*a, **k)
        self._undo_button = None
        self._redo_button = None        
        self._last_quant_value = Live.Song.RecordingQuantization.rec_q_eight
        self._on_quantization_changed.subject = self.song()
        self._update_quantization_state()
        self.set_quant_toggle_button = self.rec_quantization_button.set_control_element
        

    @rec_quantization_button.pressed
    def rec_quantization_button(self, value):
        assert self._last_quant_value != Live.Song.RecordingQuantization.rec_q_no_q
        quant_value = self.song().midi_recording_quantization
        if quant_value != Live.Song.RecordingQuantization.rec_q_no_q:
            self._last_quant_value = quant_value
            self.song().midi_recording_quantization = Live.Song.RecordingQuantization.rec_q_no_q
        else:
            self.song().midi_recording_quantization = self._last_quant_value

    @subject_slot('midi_recording_quantization')
    def _on_quantization_changed(self):
        if self.is_enabled():
            self._update_quantization_state()

    def _update_quantization_state(self):
        quant_value = self.song().midi_recording_quantization
        quant_on = quant_value != Live.Song.RecordingQuantization.rec_q_no_q
        if quant_on:
            self._last_quant_value = quant_value
        self.rec_quantization_button.color = 'DefaultButton.On' if quant_on else 'DefaultButton.Off'

    def set_undo_button(self, undo_button):
        #assert isinstance(undo_button, (ButtonCombine, type(None)))
        if (undo_button != self._undo_button):
            if (self._undo_button != None):
                self._undo_button.remove_value_listener(self._undo_value)
            self._undo_button = undo_button
            if (self._undo_button != None):
                self._undo_button.add_value_listener(self._undo_value)
            self.update()


    def _undo_value(self, value):
        assert (self._undo_button != None)
        assert (value in range(128))
        if self.is_enabled():
            if ((value != 0) or (not self._undo_button.is_momentary())):
                if self.song().can_undo:
                    self.song().undo()
                            
                            
    def set_tempo_encoder(self, control):
        assert ((control == None) or (isinstance(control, EncoderElement) and (control.message_map_mode() is Live.MidiMap.MapMode.relative_two_compliment)))
        if (self._tempo_encoder_control != None):
                self._tempo_encoder_control.remove_value_listener(self._tempo_encoder_value)
        self._tempo_encoder_control = control
        if (self._tempo_encoder_control != None):
            self._tempo_encoder_control.add_value_listener(self._tempo_encoder_value)
        self.update()
    
