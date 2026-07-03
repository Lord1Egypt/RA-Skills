from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_post_by_id_tool(
    post_id: int
) -> Dict[str, Any]:
    """
    
Retrieve a specific post by its ID.

Args:
    post_id: The ID of the post to retrieve

    
    Args:
        post_id: null
    
    Returns:
        null
    """
    arguments = {
        "post_id": post_id
    }
    
    return call_api("1777419061950467", "get_post_by_id_tool", arguments)

def search_posts(
    query: str,
    limit: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    
Search for posts/drops containing a specific keyword or phrase.

Args:
    query: The keyword or phrase to search for
    limit: Maximum number of results to return (default: 10)

    
    Args:
        query: null
        limit: null
    
    Returns:
        null
    """
    arguments = {
        "query": query,
        "limit": limit
    }
    
    return call_api("1777419061950467", "search_posts", arguments)

def get_posts_by_date(
    start_date: str,
    end_date: Optional[str] = None,
    limit: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    
Get posts/drops within a specific date range.

Args:
    start_date: Start date in YYYY-MM-DD format
    end_date: End date in YYYY-MM-DD format (defaults to start_date if not provided)
    limit: Maximum number of results to return (default: 10)

    
    Args:
        start_date: null
        end_date: null
        limit: null
    
    Returns:
        null
    """
    arguments = {
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit
    }
    
    return call_api("1777419061950467", "get_posts_by_date", arguments)

def get_posts_by_author_id(
    author_id: str,
    limit: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    
Get posts/drops by a specific author ID.

Args:
    author_id: The author ID to search for
    limit: Maximum number of results to return (default: 10)

    
    Args:
        author_id: null
        limit: null
    
    Returns:
        null
    """
    arguments = {
        "author_id": author_id,
        "limit": limit
    }
    
    return call_api("1777419061950467", "get_posts_by_author_id", arguments)

def analyze_post(
    post_id: int
) -> Dict[str, Any]:
    """
    
Get detailed analysis of a specific post/drop including references and context.

Args:
    post_id: The ID of the post to analyze

    
    Args:
        post_id: null
    
    Returns:
        null
    """
    arguments = {
        "post_id": post_id
    }
    
    return call_api("1777419061950467", "analyze_post", arguments)

def get_timeline_summary(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    
Get a timeline summary of posts/drops, optionally within a date range.

Args:
    start_date: Optional start date in YYYY-MM-DD format
    end_date: Optional end date in YYYY-MM-DD format

    
    Args:
        start_date: null
        end_date: null
    
    Returns:
        null
    """
    arguments = {
        "start_date": start_date,
        "end_date": end_date
    }
    
    return call_api("1777419061950467", "get_timeline_summary", arguments)

def word_cloud_by_post_ids(
    start_id: int,
    end_id: int,
    min_word_length: Optional[int] = 3.0,
    max_words: Optional[int] = 100.0
) -> Dict[str, Any]:
    """
    
Generate a word cloud analysis showing the most common words used in posts within a specified ID range.

Args:
    start_id: Starting post ID
    end_id: Ending post ID
    min_word_length: Minimum length of words to include (default: 3)
    max_words: Maximum number of words to return (default: 100)

    
    Args:
        start_id: null
        end_id: null
        min_word_length: null
        max_words: null
    
    Returns:
        null
    """
    arguments = {
        "start_id": start_id,
        "end_id": end_id,
        "min_word_length": min_word_length,
        "max_words": max_words
    }
    
    return call_api("1777419061950467", "word_cloud_by_post_ids", arguments)

def word_cloud_by_date_range(
    start_date: str,
    end_date: str,
    min_word_length: Optional[int] = 3.0,
    max_words: Optional[int] = 100.0
) -> Dict[str, Any]:
    """
    
Generate a word cloud analysis showing the most common words used in posts within a specified date range.

Args:
    start_date: Start date in YYYY-MM-DD format
    end_date: End date in YYYY-MM-DD format
    min_word_length: Minimum length of words to include (default: 3)
    max_words: Maximum number of words to return (default: 100)

    
    Args:
        start_date: null
        end_date: null
        min_word_length: null
        max_words: null
    
    Returns:
        null
    """
    arguments = {
        "start_date": start_date,
        "end_date": end_date,
        "min_word_length": min_word_length,
        "max_words": max_words
    }
    
    return call_api("1777419061950467", "word_cloud_by_date_range", arguments)

