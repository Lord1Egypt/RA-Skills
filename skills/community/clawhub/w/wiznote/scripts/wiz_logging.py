"""日志模块 - 所有日志必须输出到 stderr"""
import sys as _sys
from importlib import import_module
_logging = import_module('logging')

logger = _logging.getLogger("wiz_mcp")
logger.setLevel(_logging.INFO)

if not logger.handlers:
    handler = _logging.StreamHandler(_sys.stderr)
    handler.setLevel(_logging.INFO)
    formatter = _logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def get_logger():
    return logger
