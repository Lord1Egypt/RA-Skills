"""
Additional unit tests for retry logic
"""

import pytest
from unittest.mock import Mock
import time

from social_media_automation.utils.retry import retry_on_exception


def test_retry_on_exception_success():
    """Test retry logic with success on first attempt"""
    mock_func = Mock(return_value="success")

    result = retry_on_exception(
        lambda: mock_func(),
        max_retries=3,
        delay=0.01,
    )

    assert result == "success"
    assert mock_func.call_count == 1


def test_retry_on_exception_retry_once():
    """Test retry logic with success on second attempt"""
    mock_func = Mock(side_effect=[Exception("error"), "success"])

    result = retry_on_exception(
        lambda: mock_func(),
        max_retries=3,
        delay=0.01,
    )

    assert result == "success"
    assert mock_func.call_count == 2


def test_retry_on_exception_max_attempts():
    """Test retry logic exceeding max attempts"""
    mock_func = Mock(side_effect=Exception("error"))

    with pytest.raises(Exception, match="error"):
        retry_on_exception(
            lambda: mock_func(),
            max_retries=3,
            delay=0.01,
        )

    assert mock_func.call_count == 3


def test_retry_on_exception_specific_exception():
    """Test retry logic with specific exception type"""
    mock_func = Mock(side_effect=ValueError("value error"))

    # Should only retry on specific exception
    with pytest.raises(ValueError):
        retry_on_exception(
            lambda: mock_func(),
            max_retries=3,
            delay=0.01,
            exceptions=(ValueError,),
        )

    assert mock_func.call_count == 3


def test_retry_on_exception_ignoring_exceptions():
    """Test retry logic ignoring certain exceptions"""
    mock_func = Mock(side_effect=TypeError("type error"))

    # Should not retry on ignored exception
    with pytest.raises(TypeError):
        retry_on_exception(
            lambda: mock_func(),
            max_retries=3,
            delay=0.01,
            exceptions=(ValueError,),
        )

    # Should fail immediately without retry
    assert mock_func.call_count == 1


def test_retry_decorator():
    """Test RetryDecorator"""
    from social_media_automation.utils.retry import RetryDecorator

    mock_func = Mock(return_value="success")

    @RetryDecorator(max_retries=3, delay=0.01)
    def test_func():
        return mock_func()

    result = test_func()

    assert result == "success"
    assert mock_func.call_count == 1