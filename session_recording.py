# Python bytecode 2.7 (62211)
# Embedded file name: c:\lakoske\live\output\win_64_static\Release\python-bundle\MIDI Remote Scripts\iRig_Keys_IO\session_recording.py
# Compiled at: 2018-07-05 12:45:26
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import SessionRecordingComponent as SessionRecordingComponentBase
from ableton.v2.control_surface.control import ButtonControl

class SessionRecordingComponent(SessionRecordingComponentBase):
    record_stop_button = ButtonControl()

    @record_stop_button.pressed
    def record_stop_button(self, _):
        self.song.session_record = False