import sys

from je_auto_control.utils.exception.exception_tag import keyboard_hotkey
from je_auto_control.utils.exception.exception_tag import keyboard_press_key
from je_auto_control.utils.exception.exception_tag import keyboard_release_key
from je_auto_control.utils.exception.exception_tag import keyboard_type_key
from je_auto_control.utils.exception.exception_tag import keyboard_write
from je_auto_control.utils.exception.exception_tag import keyboard_write_cant_find
from je_auto_control.utils.exception.exception_tag import table_cant_find_key
from je_auto_control.utils.exception.exceptions import AutoControlCantFindKeyException
from je_auto_control.utils.exception.exceptions import AutoControlKeyboardException
from je_auto_control.wrapper.platform_wrapper import keyboard
from je_auto_control.wrapper.platform_wrapper import keyboard_check
from je_auto_control.wrapper.platform_wrapper import keys_table
from je_auto_control.utils.test_record.record_test_class import record_total


def press_key(keycode: [int, str], is_shift: bool = False, skip_record: bool = False):
    """
    use to press a key still press to use release key
    or use critical exit
    return keycode
    :param keycode which keycode we want to press
    :param is_shift press shift True or False
    :param skip_record skip record on record total list True or False
    """
    param = locals()
    try:
        if type(keycode) is not int:
            try:
                keycode = keys_table.get(keycode)
            except AutoControlCantFindKeyException:
                raise AutoControlCantFindKeyException(table_cant_find_key)
        try:
            if sys.platform in ["win32", "cygwin", "msys", "linux", "linux2"]:
                keyboard.press_key(keycode)
            elif sys.platform in ["darwin"]:
                keyboard.press_key(keycode, is_shift=is_shift)
            if not skip_record:
                record_total("press_key", param)
            return str(keycode)
        except AutoControlKeyboardException as error:
            raise AutoControlKeyboardException(keyboard_press_key + " " + repr(error))
        except TypeError as error:
            raise AutoControlKeyboardException(repr(error))
    except Exception as error:
        if not skip_record:
            record_total("press_key", param, repr(error))
        print(repr(error), file=sys.stderr)


def release_key(keycode: [int, str], is_shift: bool = False, skip_record: bool = False):
    """
    use to release pressed key return keycode
    :param keycode which keycode we want to release
    :param is_shift press shift True or False
    :param skip_record skip record on record total list True or False
    """
    param = locals()
    try:
        if type(keycode) is not int:
            try:
                keycode = keys_table.get(keycode)
            except AutoControlCantFindKeyException:
                raise AutoControlCantFindKeyException(table_cant_find_key)
        try:
            if sys.platform in ["win32", "cygwin", "msys", "linux", "linux2"]:
                keyboard.release_key(keycode)
            elif sys.platform in ["darwin"]:
                keyboard.release_key(keycode, is_shift=is_shift)
            if not skip_record:
                record_total("release_key", param)
            return str(keycode)
        except AutoControlKeyboardException as error:
            raise AutoControlKeyboardException(keyboard_release_key + " " + repr(error))
        except TypeError as error:
            raise AutoControlKeyboardException(repr(error))
    except Exception as error:
        if not skip_record:
            record_total("release_key", param, repr(error))
        print(repr(error), file=sys.stderr)


def type_key(keycode: [int, str], is_shift: bool = False, skip_record: bool = False):
    """
    press and release key return keycode
    :param keycode which keycode we want to type
    :param is_shift press shift True or False
    :param skip_record skip record on record total list True or False
    """
    param = locals()
    try:
        try:
            press_key(keycode, is_shift, skip_record=True)
            release_key(keycode, is_shift, skip_record=True)
            if not skip_record:
                record_total("type_key", param)
            return str(keycode)
        except AutoControlKeyboardException as error:
            raise AutoControlKeyboardException(keyboard_type_key + " " + repr(error))
        except TypeError as error:
            raise AutoControlKeyboardException(repr(error))
    except Exception as error:
        if not skip_record:
            record_total("type_key", param, repr(error))
        print(repr(error), file=sys.stderr)


def check_key_is_press(keycode: [int, str]):
    """
    use to check key is press return True or False
    :param keycode check key is press or not
    """
    param = locals()
    try:
        if type(keycode) is int:
            get_key_code = keycode
        else:
            get_key_code = keys_table.get(keycode)
        record_total("check_key_is_press", param)
        return keyboard_check.check_key_is_press(keycode=get_key_code)
    except Exception as error:
        record_total("check_key_is_press", param, repr(error))
        print(repr(error), file=sys.stderr)


def write(write_string: str, is_shift: bool = False):
    """
    use to press and release whole we get this function str
    return all press and release str
    :param write_string while string not on write_string+1 type_key(string)
    :param is_shift press shift True or False
    """
    param = locals()
    try:
        try:
            record_write_string = ""
            for single_string in write_string:
                try:
                    if keys_table.get(single_string) is not None:
                        record_write_string = "".join(
                            [
                                record_write_string,
                                type_key(single_string, is_shift, skip_record=True)
                            ]
                        )
                    else:
                        raise AutoControlKeyboardException(keyboard_write_cant_find)
                except AutoControlKeyboardException:
                    print(keyboard_write_cant_find, single_string, sep="\t", file=sys.stderr)
                    raise AutoControlKeyboardException(keyboard_write_cant_find)
            record_total("write", param)
            return record_write_string
        except AutoControlKeyboardException as error:
            raise AutoControlKeyboardException(keyboard_write + " " + repr(error))
    except Exception as error:
        record_total("write", param, repr(error))
        print(repr(error), file=sys.stderr)


def hotkey(key_code_list: list, is_shift: bool = False):
    """
    use to press and release all key on key_code_list
    then reverse list press and release again
    return [press_str_list, release_str_list]
    :param key_code_list press and release all key on list and reverse
    :param is_shift press shift True or False
    """
    param = locals()
    try:
        try:
            record_hotkey_press_string = ""
            record_hotkey_release_string = ""
            for key in key_code_list:
                record_hotkey_press_string = ",".join(
                    [
                        record_hotkey_press_string,
                        press_key(key, is_shift, skip_record=True)
                    ]
                )
            key_code_list.reverse()
            for key in key_code_list:
                record_hotkey_release_string = ",".join(
                    [
                        record_hotkey_release_string,
                        release_key(key, is_shift, skip_record=True)
                    ]
                )
            record_total("hotkey", param)
            return record_hotkey_press_string, record_hotkey_release_string
        except AutoControlKeyboardException as error:
            raise AutoControlKeyboardException(keyboard_hotkey + " " + repr(error))
    except Exception as error:
        record_total("hotkey", param, repr(error))
        print(repr(error), file=sys.stderr)
