"""
Additional unit tests for logger
"""

import pytest
import os
from pathlib import Path

from social_media_automation.utils.logger import setup_logger


def test_logger_creation():
    """Test logger creation"""
    logger = setup_logger()

    assert logger is not None
    assert logger.name == "social_media_automation"


def test_logger_file_creation(tmp_path):
    """Test that logger creates log file"""
    log_file = tmp_path / "test.log"

    # Set environment variable for log file
    os.environ["LOG_FILE"] = str(log_file)

    logger = setup_logger()

    # Log a message
    logger.info("Test message")

    # Check that log file was created
    assert log_file.exists()


def test_logger_levels():
    """Test logger levels"""
    logger = setup_logger()

    # Should not raise errors
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")


def test_logger_without_file():
    """Test logger without file"""
    # Remove environment variable
    if "LOG_FILE" in os.environ:
        del os.environ["LOG_FILE"]

    logger = setup_logger()

    # Should still work
    logger.info("Test message")

    assert logger is not None
