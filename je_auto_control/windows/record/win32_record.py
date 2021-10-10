import sys

if sys.platform not in ["win32", "cygwin", "msys"]:
    raise Exception("should be only loaded on windows")

from je_auto_control.windows.listener.win32_keyboard_listener import Win32KeyboardListener
from je_auto_control.windows.listener.win32_mouse_listener import Win32MouseListener

from je_auto_control.utils.je_auto_control_exception.exceptions import AutoControlRecordException

from queue import Queue


class Win32Recorder(object):

    def __init__(self):
        self.mouse_record_listener = None
        self.keyboard_record_listener = None
        self.record_queue = None
        self.result_queue = None

    def record(self):
        self.mouse_record_listener = Win32MouseListener()
        self.keyboard_record_listener = Win32KeyboardListener()
        self.record_queue = Queue()
        self.mouse_record_listener.record(self.record_queue)
        self.keyboard_record_listener.record(self.record_queue)

    def stop_record(self):
        self.result_queue =self.mouse_record_listener.stop_record()
        self.result_queue = self.keyboard_record_listener.stop_record()
        self.record_queue = None
        return self.result_queue

    def record_mouse(self):
        self.mouse_record_listener = Win32MouseListener()
        self.record_queue = Queue()
        self.mouse_record_listener.record(self.record_queue)

    def stop_record_mouse(self):
        self.result_queue = self.mouse_record_listener.stop_record()
        self.record_queue = None
        return self.result_queue

    def record_keyboard(self):
        self.keyboard_record_listener = Win32KeyboardListener()
        self.record_queue = Queue()
        self.keyboard_record_listener.record(record_queue)

    def stop_record_keyboard(self):
        self.result_queue = self.keyboard_record_listener.stop_record()
        self.record_queue = None
        return self.result_queue


win32_recorder = Win32Recorder()

if __name__ == "__main__":
    win32_recorder = Win32Recorder()
    win32_recorder.record()
    from time import sleep
    sleep(10)
    for i in win32_recorder.stop_record().queue:
        print(i)
