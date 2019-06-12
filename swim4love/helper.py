import re
import sys
import traceback
from functools import wraps

from flask import jsonify

from swim4love.site_config import SWIMMER_ID_LENGTH


def return_error_json(func):
    '''
    Catch any exception not handled and return
    the error message and line number in JSON.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            # Return the line number of the immediate cause, not the root cause
            tb = traceback.extract_tb(exc_tb)[-1]
            error_msg = 'File "{}", line {}, in {}\n    {}\n'.format(*tb)
            error_msg += '{}: {}'.format(e.__class__.__name__, str(e))
            return jsonify({'code': -1,
                            'error': error_msg,
                            'lineno': traceback.extract_tb(exc_tb)[-1].lineno})
    return wrapper


def is_valid_id(swimmer_id):
    '''
    Checks if a given swimmer ID is valid.
    '''
    # Don't use `str.isdigit()`!  For example, try `'³'.isdigit()`.
    # Don't use `str.isnumeric()`.  It allows even more characters, like '五'.
    # Use `str.isdecimal()` in this case.
    # But, for simplicity and unambiguity, we'll use regular expressions.
    # Don't use `'\d'` for regular expressions!  It allows '੩'.
    # Use `'[0-9]'`.
    return re.match(rf'[0-9]{SWIMMER_ID_LENGTH}', swimmer_id)
