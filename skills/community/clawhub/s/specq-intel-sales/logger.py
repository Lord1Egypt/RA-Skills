"""
logger.py — SpecQ v2.1 统一日志模块
"""
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stderr)],
)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
