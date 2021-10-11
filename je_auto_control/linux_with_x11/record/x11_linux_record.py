import sys

if sys.platform not in ["linux", "linux2"]:
    raise Exception("should be only loaded on linux")

from Xlib import X

from je_auto_control.linux_with_x11.listener.x11_linux_listener import x11_linux_record
from je_auto_control.linux_with_x11.listener.x11_linux_listener import x11_linux_stop_record

from queue import Queue

type_dict = {5: "mouse", 3: "keyboard"}
detail_dict = {1: "mouse_left", 2: "mouse_middle", 3: "mouse_right"}


class X11LinuxRecorder(object):

    def __init__(self):
        self.record_queue = None
        self.result_queue = None

    def record(self):
        self.record_queue = Queue()
        x11_linux_record(self.record_queue)

    def stop_record(self):
        self.result_queue = x11_linux_stop_record()
        action_queue = Queue()
        for details in self.result_queue.queue:
            if details[0] == 5:
                action_queue.put((detail_dict.get(details[1]), details[2], details[3]))
            elif details[0] == 3:
                action_queue.put((type_dict.get(details[0]), details[1]))
        return action_queue


x11_linux_recoder = X11LinuxRecorder()


if __name__ == "__main__":
    x11_record = X11LinuxRecorder()
    x11_record.record()
    from time import sleep
    sleep(10)
    temp = x11_record.stop_record()
    for action in temp.queue:
        print(action)
