# Python bytecode 2.7 (62211)
# Embedded file name: c:\Jenkins\live\output\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC_Key_25\APC_Key_25.py
# Compiled at: 2018-07-05 12:45:24
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonElement import ButtonElement
from _Framework.ComboElement import ComboElement
#from _Framework.Control import ButtonControl
#from _APC.SessionComponent import SessionComponent as SessionComponentBase

class ButtonCombine(ButtonElement):
    #slot_launch_button = ButtonControl()
    #selected_scene_launch_button = ButtonControl()
    

    
    def __init__(self, inbuttons, *a, **k):
        self.buttons=None
        self.my_listener=None
        self.set_buttons(inbuttons)
        self=inbuttons[0]
        #super(ButtonCombine, self).__init__(*a, **k)
        
        
        #self._old_ispresed=super(ButtonElement, self).is_pressed
     #   super(ButtonElement, self).__init__(msg_type, channel, identifier, *a, **k)
     
    def _old_ispresed(self):
        super().is_pressed()
        return
    
    def add_value_listener(self, value):
        #self.show_message('listen')
        self.my_listener=value
        self.buttons[0].add_value_listener(self._main_listener, identify_sender = False)
        return
    
    def _main_listener(self, *a, **k):
        if self.is_pressed():
            self.my_listener()
            self.buttons[0]._is_pressed=False
            self.buttons[0].__is_momentary=False        
        
        return
        
        
       
    
    def set_buttons(self, buttons):
        self.buttons=buttons
        return True
    
    def is_pressed(self):
        #super().show_message('Sucsess!!!')
        for but in self.buttons:
            if not but.is_pressed():
                #self.canonical_parent.show_message('Sucsess')
                return False

        return True
            


    
            
        
        
        
        

