# Python bytecode 2.7 (62211)
# Embedded file name: c:\lakoske\live\output\win_64_static\Release\python-bundle\MIDI Remote Scripts\iRig_Keys_IO\session_recording.py
# Compiled at: 2018-07-05 12:45:26
from _Framework.SessionComponent import SessionComponent
from _Framework.SceneComponent import SceneComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.SubjectSlot import subject_slot
import time

#from _Framework.ControlSurface import ControlSurface #for log
#from _Framework.ControlSurface import log_message
import logging, traceback, Live
from _Framework.Util import lazy_attribute, nop, const, second, print_message
from .Debug import debug_print
logger = logging.getLogger(__name__)


class leClipSlotComponent(ClipSlotComponent):
    startTime=0
    delTime=0
    delnow=False
    
    
    def log_message(self, *message):
        u""" Writes the given message into Live's main log file """
        message = '(%s) %s' % (self.__class__.__name__, (' ').join(map(str, message)))
        console_message = 'LOG: ' + message
        logger.info(console_message)
        
#        if self._c_instance:
#            self._c_instance.log_message(message)


    @subject_slot('value')
    def _launch_button_value(self, value):
	
	#delnow=(time.time()-self.startTime)>.5?False:True
        
        if self.is_enabled():
	    #if self._feedback_value()!=self._triggered_to_play_value and (time.time()-self.delTime)>.5: self.delnow=False
            if self._select_button and self._select_button.is_pressed() and value:
                self._do_select_clip(self._clip_slot)
            elif self._clip_slot != None:
                if self._duplicate_button and self._duplicate_button.is_pressed():
                    if value:
                        self._do_duplicate_clip()
                elif self._delete_button and self._delete_button.is_pressed():
                    if value:
                        self._do_delete_clip()
			
                elif self._launch_button_value.subject.is_pressed():
                    
                    self.log_message("lakoske: ", str(self._feedback_value()))
                    #self.log_message("lakoske: ", str(time.time()-self.startTime)) 
		    #and self._feedback_value()!=self._triggered_to_play_value
                    if self._clip_slot and self._clip_slot.has_clip and (time.time()-self.startTime)<.4:
                        self.log_message("lakoske: ", "delete") 
			self._do_delete_clip()
			self.delnow=True;
			self.delTime=time.time()
                    elif self._feedback_value()!=self._started_value:
                        self.log_message("lakoske: ", "Start") 
                        if self._feedback_value()==self._recording_value: 
			    self.log_message("lakoske: ", "Recording in progress")
			    self.stop_rec()			    
			self._do_launch_clip(value)
		    
                    else:
                        self.stop_clip()     
                    #self.stop_clip()
                    #self.song().stop_all_clips()
                    self.startTime=time.time()
                                
        return
    
    def stop_rec(self):
	self.song().session_record=False
        pass
    	return

    
    

 
    def _do_launch_clip(self, value):
	if (time.time()-self.delTime>1):
	    button = self._launch_button_value.subject
	    object_to_launch = self._clip_slot
	    launch_pressed = value or not button.is_momentary()
	    if self.has_clip():
		object_to_launch = self._clip_slot.clip
	    else:
		self._has_fired_slot = True
	    if button.is_momentary():
		object_to_launch.set_fire_button_state(value != 0)
	    else:
		if launch_pressed:
		    object_to_launch.fire()
	    if launch_pressed and self.has_clip() and self.song().select_on_launch:
		self.song().view.highlighted_clip_slot = self._clip_slot

    def stop_clip(self):
        track=self._clip_slot.canonical_parent
        track.stop_all_clips()        
        return   
    
#    def log(self, message):
#        sys.stderr.write("LOG: " + message.encode("utf-8"))
        
        
# ################################################################        




class leSceneComponent(SceneComponent):
    clip_slot_component_type = leClipSlotComponent

class leSessionComponent(SessionComponent):
    scene_component_type = leSceneComponent

    
    def set_clip_stop_buttons(self, buttons):
        assert not buttons or buttons.width() == self._num_tracks and buttons.height() == self._num_scenes
        if buttons:
            for button, (x, y) in buttons.iterbuttons():
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_launch_button(button)

        else:
            for x, y in product(xrange(self._num_tracks), xrange(self._num_scenes)):
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_launch_button(None)

        return    
    
    def set_stop_track_clip_buttons(self, buttons):
        self._stop_track_clip_buttons = buttons
        self._on_stop_track_value.replace_subjects(buttons or [])
        self._update_stop_track_clip_buttons()    

    