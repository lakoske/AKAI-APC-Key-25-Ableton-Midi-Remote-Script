# Python bytecode 2.7 (62211)
# Embedded file name: c:\Jenkins\live\output\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC_Key_25\APC_Key_25.py
# Compiled at: 2018-07-05 12:45:24

#for Ableton 11
# Edited by Dmitry Lozinsky / lakoske@gmail.com
# 3 scenes in session
# _track_modes changed by mixer component
# 4th row - solo
# 5th row - mute
# All new shortcuts in readme.txt

from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import OptimizedControlSurface
from _Framework.ComboElement import ComboElement, DoublePressElement
from _Framework.Layer import Layer
from _Framework.ModesComponent import AddLayerMode, ModesComponent
#from _Framework.SessionComponent import SessionComponent
from .leSessionComponent import leSessionComponent    #lakoske
from _Framework.Resource import SharedResource
from _Framework.Util import nop
from _Framework.TransportComponent import TransportComponent
from _Framework.SessionRecordingComponent import SessionRecordingComponent  #lakoske
from _Framework.ClipCreator import ClipCreator                              #lakoske
from .ShiftTransportComponent import ShiftTransportComponent             #lakoske
from _APC.DetailViewCntrlComponent import DetailViewCntrlComponent          #lakoske
from .button_combine import ButtonCombine
from _APC.APC import APC, MANUFACTURER_ID
from _APC.ControlElementUtils import make_button, make_knob, make_pedal_button
from _APC.DeviceComponent import DeviceComponent
from .leSkinDefault import make_default_skin, make_biled_skin, make_stop_button_skin, make_red_skin
from .SendToggleComponent import SendToggleComponent
from .MixerComponent import MixerComponent

class APC_Key_25(APC, OptimizedControlSurface):
    u""" Script for Akai's APC_Key_25 Controller """
    SESSION_WIDTH = 8
    SESSION_HEIGHT = 3
    AlwaysSolo = [0,0,1,1,0,0,0,0]
    HAS_TRANSPORT = True


    def make_shifted_button(self, button):
        return ComboElement(button, modifiers=[self._shift_button])

    @classmethod
    def wrap_matrix(cls, control_list, wrapper=nop):
        return ButtonMatrixElement(rows=[list(map(wrapper, control_list))])

    def __init__(self, *a, **k):
        super(APC_Key_25, self).__init__(*a, **k)
        self._suppress_session_highlight = False
        self._suppress_send_midi = False
        self._color_skin = make_biled_skin()
        self._default_skin = make_default_skin()
        self._stop_button_skin = make_stop_button_skin()
        self._red_skin=make_red_skin
        with self.component_guard():
            self._create_controls()
            self._session = self._create_session()
            self._session.set_stop_clip_triggered_value(True)
            self._mixer = self._create_mixer()
            self._device = self._create_device_component()
            if self.HAS_TRANSPORT:
                self._transport = self._create_transport()
                self._create_recording()        #lakoske
            self.set_device_component(self._device)
            self._session.set_mixer(self._mixer)
            self._encoder_modes = self._create_encoder_modes()
            #self._track_modes = self._create_track_button_modes() lakoske
            self.log_message("lakoske: ", "check")
#lakoske
    def _create_recording(self):
        self._transport.set_overdub_button(self._session_record_button)
##########

    def get_matrix_button(self, column, row):
        return self._matrix_buttons[row][column]

    def _create_controls(self):

        make_on_off_button = partial(make_button, skin=self._default_skin)
        make_color_button = partial(make_button, skin=self._color_skin)
        make_stop_button = partial(make_button, skin=self._stop_button_skin)
        make_solo_button = partial(make_button, skin=self._red_skin)

        self._shift_button = make_button(0, 98, resource_type=SharedResource, name='Shift_Button')
        self._parameter_knobs = [make_knob(0, (index + 48), name=('Parameter_Knob_%d' % (index + 1))) for index in range(self.SESSION_WIDTH)]
        self._select_buttons = [make_stop_button(0, (64 + index), name=('Track_Select_%d' % (index + 1))) for index in range(self.SESSION_WIDTH)]
        

        self._lesolobuttons=[ make_solo_button(0, 8 + index, name='Track_Solo_%d' % (index + 1)) for index in range(self.SESSION_WIDTH)]
        self._lemutebuttons=[ make_stop_button(0, 0 + index, name='Track_Mute_%d' % (index + 1)) for index in range(self.SESSION_WIDTH)]

        self._up_button = self.make_shifted_button(self._select_buttons[0])
        self._down_button = self.make_shifted_button(self._select_buttons[1])
        self._left_button = self.make_shifted_button(self._select_buttons[2])
        self._right_button = self.make_shifted_button(self._select_buttons[3])
        self._volume_button = self.make_shifted_button(self._select_buttons[4])
        self._pan_button = self.make_shifted_button(self._select_buttons[5])
        self._send_button = self.make_shifted_button(self._select_buttons[6])
        self._device_button = self.make_shifted_button(self._select_buttons[7])
        if self.HAS_TRANSPORT:
            self._play_button = make_on_off_button(0, 91, name='Play_Button')
            self._session_record_button = make_color_button    (0, 93, name='Session_Record_Button')
            self._record_button = self.make_shifted_button(self._session_record_button)    #lakoske
            #self._record_button=DoublePressElement(self._session_record_button)
            #self._arm_button = make_on_off_button    (0, 93, name='Arm_Button')
            #self._record_button = make_on_off_button    (0, 93, name='Record_Button')
            #self._session_recording = SessionRecordingComponent(ClipCreator(), self._view_control, name='Session_Recording', is_enabled=False, layer=Layer(record_button=arm_button))
            #self._session_recording = self._arm_button   #lakoske
            # self._session_recording.layer = Layer(record_button=self._arm_button)           #lakoske

        def matrix_note(x, y):
            return x + self.SESSION_WIDTH * (self.SESSION_HEIGHT - y - 1)

        self._matrix_buttons = [ [ make_color_button(0, matrix_note(track, scene)+(40-self.SESSION_WIDTH*self.SESSION_HEIGHT), name='%d_Clip_%d_Button' % (track, scene)) for track in range(self.SESSION_WIDTH) ] for scene in range(self.SESSION_HEIGHT)] #lakoske +8
        self._session_matrix = ButtonMatrixElement(name='Button_Matrix', rows=self._matrix_buttons)
        self._scene_launch_buttons = [make_color_button(0, index+82, name='Scene_Launch_%d' % (index + 1)) for index in range(self.SESSION_HEIGHT)]

        self._leMuteBut=make_stop_button(0, 85, name='leMuteBut')
        self._leSelectBut=make_stop_button(0, 86, name='leSelectBut')

        self._stop_button = self.make_shifted_button(self._scene_launch_buttons[0])
        self._solo_button = self.make_shifted_button(self._scene_launch_buttons[1])
        self._arm_button = self.make_shifted_button(self._scene_launch_buttons[2])
        self._mute_button = self.make_shifted_button(self._leMuteBut)

        #self._solo_button=self._arm_button
        #self._mute_button=self._arm_button

        self._select_button = self.make_shifted_button(self._leSelectBut)
        #self._leSelectBut=make_color_button(0, 90, name="SceneLaunch4")
        self._leSelectBut.add_value_listener(self._undo_func, identify_sender = True)              #lakoske

        self._null_button=make_button(1, 64, name='Null_Button')
        self._stop_all_button = make_button(0, 81, resource_type=SharedResource, name='Stop_All_Clips_Button')
        self._stop_all_button.add_value_listener(self._press_stop, identify_sender = False) #lakoske
        self._metronome_button = self._stop_button

        self._shift_button.add_value_listener(self._press_shift, identify_sender = False)

        #self._clip_delete_button.add_value_listener(self._do_delete_clip, identify_sender = False)


        #self._clip_delete_button = self.make_shifted_button(self._stop_all_button)                          #lakoske
        #self._clip_delete_button=button_combine(self._stop_all_button, self._shift_button)
        #self._clip_delete_button.add_value_listener(self._do_delete_clip, identify_sender = False)              #lakoske
        #self._session_record_button.add_value_listener(self.arm_rec_proc, identify_sender = False)          #lakoske




    def _undo_func(self,value, *a, **b):
        self.show_message('undO')
        if  self._shift_button.is_pressed():
            if self.song().can_undo:
                self.song().undo()
            self._leSelectBut._is_pressed=False
            self._leSelectBut.__is_momentary=False
            self._leSelectBut._last_received_value=0
            self._leSelectBut.turn_off()
        return

    #__________________________________________________________
    def _press_shift (self,value):
        if  self._shift_button.is_pressed():
            self._leSelectBut.clear_value_listeners()
            self._leSelectBut.add_value_listener(self._undo_func, identify_sender = False)
            self._transport.set_overdub_button(self._null_button)
        else:
            self._leSelectBut.clear_value_listeners()
            self._session.set_scene_launch_buttons(self.wrap_matrix(self._scene_launch_buttons))
            self._transport.set_overdub_button(self._session_record_button)

        self.make_del_but(value)
        return

    def _press_stop(self,value):
        self.make_del_but(value)
        return

    def make_del_but(self,value):
        if self._shift_button.is_pressed() and self._stop_all_button.is_pressed():
            self._session.set_stop_all_clips_button(self._null_button)
            for scene_index in range(self.SESSION_HEIGHT):
                for track_index in range(self.SESSION_WIDTH):
                    slot = self._session.scene(scene_index).clip_slot(track_index)
                    slot.set_select_button(self._null_button)
                    slot.set_delete_button(self._stop_all_button)
        else:
            for scene_index in range(self.SESSION_HEIGHT):
                for track_index in range(self.SESSION_WIDTH):
                    slot = self._session.scene(scene_index).clip_slot(track_index)
                    slot.set_select_button(self._shift_button)
                    slot.set_delete_button(self._null_button)
            self._session.set_stop_all_clips_button(self._stop_all_button)

        return


    def _do_delete_clip(self,value):
        self.show_message('delete')
        if self._clip_slot and self._clip_slot.has_clip:
            self._clip_slot.delete_clip()
        return
    #__________________________________________________________


    def _make_stop_all_button(self):
        return make_button(0, 81, name='Stop_All_Clips_Button')

    def _create_session(self):
        session = leSessionComponent((self.SESSION_WIDTH),
            (self.SESSION_HEIGHT),
            auto_name=True,
            enable_skinning=True,
            is_enabled=False, 
            layer=Layer(scene_launch_buttons=(self.wrap_matrix(self._scene_launch_buttons)), 
            clip_launch_buttons=(self._session_matrix),  
            track_bank_left_button=(self._left_button),
            track_bank_right_button=(self._right_button),
            scene_bank_up_button=(self._up_button),
            scene_bank_down_button=(self._down_button)))
        #session.set_stop_track_clip_buttons(self._session_matrix)
        #self.session.set_stop_clip_value()
        for scene_index in range(self.SESSION_HEIGHT):
            for track_index in range(self.SESSION_WIDTH):
                slot = session.scene(scene_index).clip_slot(track_index)
                slot.layer = Layer( select_button=self._shift_button)#, delete_button=self._clip_delete_button) #select_button=self._shift_button,
        session.set_stop_all_clips_button(self._stop_all_button)
                #slot.set_delete_button(self._stop_all_button)
        return session

    def _create_mixer(self):
        solo_button_matrix = self.wrap_matrix(self._lesolobuttons)
        mute_button_matrix = self.wrap_matrix(self._lemutebuttons)
        return MixerComponent(self.SESSION_WIDTH, auto_name=True, is_enabled=False, invert_mute_feedback=True, layer=Layer(solo_buttons=solo_button_matrix, mute_buttons=mute_button_matrix, arm_buttons=self.wrap_matrix(self._select_buttons)))

    def _create_device_component(self):
        return DeviceComponent(name='Device_Component', is_enabled=False, device_selection_follows_track_selection=True)

    def _create_transport(self):

        def play_toggle_model_transform(value):
            if self._shift_button.is_pressed():
                return False
            return value
        transport=TransportComponent(name='Transport', is_enabled=False, play_toggle_model_transform=play_toggle_model_transform, layer=Layer(play_button=self._play_button, record_button=self._record_button, metronome_button=self._metronome_button))
        return transport



    def _create_encoder_modes(self):
        knob_modes = ModesComponent(name='Knob Modes', is_enabled=False)
        parameter_knobs_matrix = self.wrap_matrix(self._parameter_knobs)
        send_toggle_component = SendToggleComponent(self._mixer, name='Toggle Send', is_enabled=False, layer=Layer(toggle_button=self._send_button, priority=1))
        knob_modes.add_mode('volume', AddLayerMode(self._mixer, Layer(volume_controls=parameter_knobs_matrix)))
        knob_modes.add_mode('pan', AddLayerMode(self._mixer, Layer(pan_controls=parameter_knobs_matrix)))
        knob_modes.add_mode('send', [
         AddLayerMode(self._mixer, Layer(send_controls=parameter_knobs_matrix)),
         send_toggle_component])
        knob_modes.add_mode('device', AddLayerMode(self._device, Layer(parameter_controls=parameter_knobs_matrix)))
        knob_modes.selected_mode = 'device'
        knob_modes.layer = Layer(volume_button=self._volume_button, pan_button=self._pan_button, send_button=self._send_button, device_button=self._device_button)
        return knob_modes

    def _create_track_button_modes(self):
        track_button_modes = ModesComponent(name='Track Button Modes', is_enabled=False)
        select_button_matrix = self.wrap_matrix(self._select_buttons)

        solo_button_matrix = self.wrap_matrix(self._lesolobuttons)
        mute_button_matrix = self.wrap_matrix(self._lemutebuttons)

        track_button_modes.add_mode('clip_stop', AddLayerMode(self._session, Layer(stop_track_clip_buttons=select_button_matrix)))
        track_button_modes.add_mode('solo', AddLayerMode(self._mixer, layer=Layer(solo_buttons=solo_button_matrix)))
        track_button_modes.add_mode('arm', AddLayerMode(self._mixer, layer=Layer(arm_buttons=select_button_matrix)))
        track_button_modes.add_mode('mute', AddLayerMode(self._mixer, layer=Layer(mute_buttons=mute_button_matrix  )))
        #track_button_modes.add_mode('select', AddLayerMode(self._mixer, layer=Layer(track_select_buttons=select_button_matrix)))
        track_button_modes.selected_mode = 'arm'
        track_button_modes.layer = Layer(solo_button=self._solo_button, arm_button=self._arm_button, mute_button=self._mute_button) #, select_button=self._select_button, clip_stop_button=self._stop_button)
        return track_button_modes

    def _set_components_enabled(self, enable):
        with self.component_guard():
            self._session.set_enabled(enable)
            self._mixer.set_enabled(enable)
            self._device.set_enabled(enable)
            if self.HAS_TRANSPORT:
                self._transport.set_enabled(enable)
            self._encoder_modes.set_enabled(enable)
            #self._track_modes.set_enabled(enable)	lakoske

    def _should_combine(self):
        return False

    def _update_hardware(self):
        self.set_highlighting_session_component(None)
        self._set_components_enabled(False)
        self._send_midi((240, 126, 127, 6, 1, 247))
        return

    def _product_model_id_byte(self):
        return 39

    def _on_identity_response(self, midi_bytes):
        super(APC_Key_25, self)._on_identity_response(midi_bytes)
        if midi_bytes[5] == MANUFACTURER_ID and midi_bytes[6] == self._product_model_id_byte():
            self._set_components_enabled(True)
            self.set_highlighting_session_component(self._session)

    def _send_dongle_challenge(self):
        pass

    def _on_handshake_successful(self):
        pass
