import logging
import os
import os.path
import sys
from functools import lru_cache, wraps
from typing import *

import click


def retries(func, retry: int = 3):
    @wraps(func)
    def retries_wrapper(*args, n_retries: int = retry, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if n_retries > 0:
                return retries_wrapper(*args, n_retries=n_retries - 1, **kwargs)
            else:
                raise e

    return retries_wrapper


def logger(obj: Union[str, object] = 'v5') -> logging.Logger:
    if isinstance(obj, str):
        return logging.getLogger(obj)
    return logging.getLogger(obj.__module__)


def isdebug(obj: Union[str, object] = 'v5') -> bool:
    if obj is None:
        obj = 'v5'
    if isinstance(obj, str):
        return logging.getLogger(obj).getEffectiveLevel() == logging.DEBUG
    return logging.getLogger(obj.__module__).getEffectiveLevel() == logging.DEBUG


def ismachineoutput(ctx: click.Context = None) -> bool:
    if ctx is None:
        ctx = click.get_current_context(silent=True)
    if isinstance(ctx, click.Context):
        ctx.ensure_object(dict)
        assert isinstance(ctx.obj, dict)
        return ctx.obj.get('machine_output', False)
    else:
        return False

def dont_send(e: Exception):
    e.sentry = False
    return e
