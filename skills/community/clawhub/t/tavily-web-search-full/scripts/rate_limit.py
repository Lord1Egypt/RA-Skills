#!/usr/bin/env python3
"""
Rate Limit Handler for Tavily APIs
Handles 429 Too Many Requests errors with exponential backoff and retry-after support.

Based on: https://docs.tavily.com/documentation/rate-limits.md

Rate Limits:
- Search/Extract/Map: 100 RPM (dev) / 1,000 RPM (prod)
- Crawl: 100 RPM (both)
- Research: 20 RPM (both)
- Usage: 10 requests per 10 minutes (both)
"""
import time
from datetime import datetime
from typing import Optional, Callable, Any
import functools


class RateLimitError(Exception):
    """Raised when rate limit is exceeded and max retries exhausted"""
    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message)
        self.retry_after = retry_after


def parse_retry_after(retry_after_header: Optional[str]) -> int:
    """
    Parse retry-after header value.
    Can be either seconds (int) or HTTP date string.
    
    Returns seconds to wait.
    """
    if not retry_after_header:
        return 60  # Default to 60 seconds
    
    # Try parsing as integer (seconds)
    try:
        return int(retry_after_header)
    except ValueError:
        pass
    
    # Try parsing as HTTP date
    try:
        from email.utils import parsedate_to_datetime
        retry_date = parsedate_to_datetime(retry_after_header)
        delta = retry_date - datetime.now(tz=retry_date.tzinfo)
        return max(1, int(delta.total_seconds()))
    except Exception:
        pass
    
    # Fallback
    return 60


def rate_limit_handler(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 300.0,
    exponential_base: float = 2.0,
    log_func: Optional[Callable[[str, str], None]] = None
):
    """
    Decorator for handling rate limits with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds for exponential backoff
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff
        log_func: Optional logging function (message, level)
    
    Usage:
        @rate_limit_handler(max_retries=3, log_func=log)
        def api_call():
            # Your API call here
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_error = None
            
            for attempt in range(1, max_retries + 1):
                try:
                    if log_func:
                        log_func(f"Request attempt {attempt}/{max_retries}", "DEBUG")
                    
                    return func(*args, **kwargs)
                    
                except urllib.error.HTTPError as e:
                    if e.code == 429:
                        # Rate limited
                        retry_after = None
                        
                        # Try to get retry-after header
                        if hasattr(e, 'headers') and 'retry-after' in e.headers:
                            retry_after = parse_retry_after(e.headers['retry-after'])
                        
                        if attempt < max_retries:
                            # Calculate delay
                            if retry_after:
                                delay = retry_after
                            else:
                                # Exponential backoff
                                delay = min(base_delay * (exponential_base ** (attempt - 1)), max_delay)
                            
                            if log_func:
                                log_func(f"Rate limited. Waiting {delay:.1f}s before retry...", "WARN")
                            
                            time.sleep(delay)
                            continue
                        else:
                            last_error = RateLimitError(
                                f"Rate limit exceeded after {max_retries} attempts",
                                retry_after=retry_after
                            )
                            break
                    else:
                        # Other HTTP error, don't retry
                        raise
                        
                except Exception as e:
                    # Non-rate-limit error
                    last_error = e
                    if attempt < max_retries:
                        delay = min(base_delay * (exponential_base ** (attempt - 1)), max_delay)
                        if log_func:
                            log_func(f"Error (attempt {attempt}): {e}. Retrying in {delay:.1f}s...", "WARN")
                        time.sleep(delay)
                    else:
                        break
            
            # All retries exhausted
            if last_error:
                if log_func:
                    log_func(f"All {max_retries} retries failed: {last_error}", "ERROR")
                raise last_error
            else:
                raise RateLimitError("Unknown error after retries")
        
        return wrapper
    return decorator


# Import urllib for type hints in decorator
import urllib.error
