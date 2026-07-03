from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def lowercase(
    text: str
) -> Dict[str, Any]:
    """
    Convert text to lowercase
    
    Args:
        text: Text to convert to lowercase
    
    Returns:
        null
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659708931", "lowercase", arguments)

def uppercase(
    text: str
) -> Dict[str, Any]:
    """
    Convert text to uppercase
    
    Args:
        text: Text to convert to uppercase
    
    Returns:
        null
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659708931", "uppercase", arguments)

def reverse(
    text: str
) -> Dict[str, Any]:
    """
    Reverse the order of characters in text
    
    Args:
        text: Text to reverse
    
    Returns:
        null
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659708931", "reverse", arguments)

def isPalindrome(
    text: str,
    ignoreSpaces: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Check if text is a palindrome (reads the same forwards and backwards)
    
    Args:
        text: Text to check
        ignoreSpaces: Ignore spaces and punctuation (default: false)
    
    Returns:
        null
    """
    arguments = {
        "text": text,
        "ignoreSpaces": ignoreSpaces
    }
    
    return call_api("1777316659708931", "isPalindrome", arguments)

def countWords(
    text: str
) -> Dict[str, Any]:
    """
    Count the number of words in text
    
    Args:
        text: Text to count words in
    
    Returns:
        null
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659708931", "countWords", arguments)

def countCharacters(
    text: str,
    includeSpaces: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Count the number of characters in text
    
    Args:
        text: Text to count characters in
        includeSpaces: Include spaces in count (default: true)
    
    Returns:
        null
    """
    arguments = {
        "text": text,
        "includeSpaces": includeSpaces
    }
    
    return call_api("1777316659708931", "countCharacters", arguments)

def trim(
    text: str
) -> Dict[str, Any]:
    """
    Remove leading and trailing whitespace from text
    
    Args:
        text: Text to trim
    
    Returns:
        null
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659708931", "trim", arguments)

def capitalize(
    text: str
) -> Dict[str, Any]:
    """
    Capitalize the first letter of each word
    
    Args:
        text: Text to capitalize
    
    Returns:
        null
    """
    arguments = {
        "text": text
    }
    
    return call_api("1777316659708931", "capitalize", arguments)

