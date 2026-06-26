"""
Logging configuration for social media automation
"""

import logging
from pathlib import Path
from typing import Any


def setup_logger(name: str = "social_media_automation", level: int = logging.INFO) -> logging.Logger:
    """Set up logger with file and console handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # File handler
    file_handler = logging.FileHandler(log_dir / "social_media_automation.log")
    file_handler.setLevel(level)
    file_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_format)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_format = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def log_api_call(logger: logging.Logger, endpoint: str, params: dict[str, Any]) -> None:
    """Log API call"""
    logger.info(f"API call: {endpoint}")
    logger.debug(f"Parameters: {params}")


def log_api_response(
    logger: logging.Logger,
    endpoint: str,
    status_code: int,
    response: Any,
) -> None:
    """Log API response"""
    logger.info(f"API response: {endpoint} - Status: {status_code}")
    logger.debug(f"Response: {response}")
