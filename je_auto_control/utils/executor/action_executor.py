import sys
import types

from je_auto_control import press_key, release_key, hotkey, type_key, write, record, stop_record
from je_auto_control import locate_all_image, locate_and_click, locate_image_center
from je_auto_control import check_key_is_press, position, press_mouse, release_mouse, click_mouse, scroll
from je_auto_control import set_position
from je_auto_control import screenshot, size
from je_auto_control.utils.exception.exception_tag import action_is_null_error, add_command_exception_tag, \
    executor_list_error
from je_auto_control.utils.exception.exception_tag import cant_execute_action_error
from je_auto_control.utils.exception.exceptions import AutoControlActionException, AutoControlAddCommandException
from je_auto_control.utils.exception.exceptions import AutoControlActionNullException
from je_auto_control.utils.html_report.html_report_generate import generate_html
from je_auto_control.utils.json.json_file import read_action_json
from je_auto_control.utils.test_record.record_test_class import record_action_to_list, test_record_instance
from je_auto_control.wrapper.auto_control_keyboard import get_special_table, get_keys_table
from je_auto_control.wrapper.auto_control_mouse import get_mouse_table


class Executor(object):

    def __init__(self):
        self.event_dict: dict = {
            # mouse
            "mouse_left": click_mouse,
            "mouse_right": click_mouse,
            "mouse_middle": click_mouse,
            "click_mouse": click_mouse,
            "mouse_table": get_mouse_table,
            "position": position,
            "press_mouse": press_mouse,
            "release_mouse": release_mouse,
            "scroll": scroll,
            "set_position": set_position,
            "special_table": get_special_table,
            # keyboard
            "keys_table": get_keys_table,
            "type_key": type_key,
            "press_key": press_key,
            "release_key": release_key,
            "check_key_is_press": check_key_is_press,
            "write": write,
            "hotkey": hotkey,
            # image
            "locate_all_image": locate_all_image,
            "locate_image_center": locate_image_center,
            "locate_and_click": locate_and_click,
            # screen
            "size": size,
            "screenshot": screenshot,
            # test record
            "set_record_enable": test_record_instance.set_record_enable,
            # generate html
            "generate_html": generate_html,
            # record
            "record": record,
            "stop_record": stop_record,
        }

    def _execute_event(self, action: list):
        event = self.event_dict.get(action[0])
        if len(action) == 2:
            return event(**action[1])
        elif len(action) == 1:
            return event()
        else:
            raise AutoControlActionException(cant_execute_action_error + " " + str(action))

    def execute_action(self, action_list: [list, dict]) -> dict:
        """
        use to execute all action on action list(action file or program list)
        :param action_list the list include action
        for loop the list and execute action
        """
        if type(action_list) is dict:
            action_list: list = action_list.get("auto_control", None)
            if action_list is None:
                raise AutoControlActionNullException(executor_list_error)
        execute_record_dict = dict()
        try:
            if len(action_list) > 0 or type(action_list) is list:
                pass
            else:
                raise AutoControlActionNullException(action_is_null_error)
        except Exception as error:
            record_action_to_list("execute_action", action_list, repr(error))
            print(repr(error), file=sys.stderr, flush=True)
        for action in action_list:
            try:
                event_response = self._execute_event(action)
                execute_record = "execute: " + str(action)
                execute_record_dict.update({execute_record: event_response})
            except Exception as error:
                print(repr(error), file=sys.stderr, flush=True)
                print(action, file=sys.stderr, flush=True)
                record_action_to_list("execute_action", None, repr(error))
                execute_record = "execute: " + str(action)
                execute_record_dict.update({execute_record: repr(error)})
        for key, value in execute_record_dict.items():
            print(key, flush=True)
            print(value, flush=True)
        return execute_record_dict

    def execute_files(self, execute_files_list: list) -> list:
        """
        :param execute_files_list: list include execute files path
        :return: every execute detail as list
        """
        execute_detail_list: list = list()
        for file in execute_files_list:
            execute_detail_list.append(self.execute_action(read_action_json(file)))
        return execute_detail_list


executor = Executor()


def add_command_to_executor(command_dict: dict):
    for command_name, command in command_dict.items():
        if isinstance(command, (types.MethodType, types.FunctionType)):
            executor.event_dict.update({command_name: command})
        else:
            raise AutoControlAddCommandException(add_command_exception_tag)


def execute_action(action_list: list) -> dict:
    return executor.execute_action(action_list)


def execute_files(execute_files_list: list) -> list:
    return executor.execute_files(execute_files_list)
