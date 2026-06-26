#!/usr/bin/env python3
"""
Tavily Resilient Request Utility
Author: Simon-Pierre Boucher
Description: Provides a robust wrapper for Tavily API requests, implementing exponential backoff
             and jitter to gracefully handle 429 Rate Limit errors and 5xx transient server errors.
"""

import time
import random
import logging
import requests
from tavily import TavilyClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TavilyResilientClient")

class TavilyRateLimitError(Exception):
    def __init__(self, retry_after, message="Tavily API Rate Limit Exceeded"):
        self.retry_after = retry_after
        super().__init__(message)

def execute_resilient_search(client: TavilyClient, query: str, max_retries: int = 5, **kwargs):
    """
    Executes a search query with exponential backoff and jitter.
    """
    base_delay = 2.0
    for attempt in range(1, max_retries + 1):
        try:
            response = client.search(query=query, **kwargs)
            return response
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else 500
            
            if status_code == 429:
                retry_after = int(e.response.headers.get("retry-after", 60)) if e.response else 60
                logger.warning(f"Rate limit hit (429). Attempt {attempt}/{max_retries}. Retrying after {retry_after}s.")
                time.sleep(retry_after)
                continue
                
            elif status_code in [500, 502, 503, 504] and attempt < max_retries:
                # Exponential backoff with full jitter
                delay = (base_delay * (2 ** (attempt - 1))) + random.uniform(0, 1.0)
                logger.warning(f"Transient server error ({status_code}). Attempt {attempt}/{max_retries}. Retrying in {delay:.2f}s.")
                time.sleep(delay)
                continue
            
            raise e
        except Exception as e:
            if attempt == max_retries:
                raise e
            delay = (base_delay * (2 ** (attempt - 1))) + random.uniform(0, 1.0)
            logger.warning(f"Unexpected error: {str(e)}. Attempt {attempt}/{max_retries}. Retrying in {delay:.2f}s.")
            time.sleep(delay)

if __name__ == "__main__":
    # Quick self-test placeholder
    print("Resilient Request Utility compiled successfully.")
