"""
Retry logic for API calls
"""

import time
from typing import Any, Callable

from social_media_automation.utils.logger import setup_logger

logger = setup_logger()


def retry_on_exception(
    func: Callable[..., Any],
    max_retries: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Any:
    """Retry a function on exception with exponential backoff"""
    last_exception = None

    for attempt in range(max_retries):
        try:
            return func()
        except exceptions as e:
            last_exception = e
            if attempt < max_retries - 1:
                wait_time = delay * (backoff_factor**attempt)
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time:.2f}s...")
                time.sleep(wait_time)
            else:
                logger.error(f"All {max_retries} attempts failed: {e}")

    raise last_exception if last_exception else Exception("Retry failed")


class RetryDecorator:
    """Decorator for retry logic"""

    def __init__(
        self,
        max_retries: int = 3,
        delay: float = 1.0,
        backoff_factor: float = 2.0,
        exceptions: tuple[type[Exception], ...] = (Exception,),
    ):
        self.max_retries = max_retries
        self.delay = delay
        self.backoff_factor = backoff_factor
        self.exceptions = exceptions

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            def attempt() -> Any:
                return func(*args, **kwargs)

            return retry_on_exception(
                attempt,
                max_retries=self.max_retries,
                delay=self.delay,
                backoff_factor=self.backoff_factor,
                exceptions=self.exceptions,
            )

        return wrapper
