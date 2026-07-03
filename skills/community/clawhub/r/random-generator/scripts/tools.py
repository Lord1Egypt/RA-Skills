from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def generate_random_integer(
    min: Optional[int] = 0.0,
    max: Optional[int] = 100.0,
    count: Optional[int] = 1.0
) -> Dict[str, Any]:
    """
    Generate cryptographically secure random integers within a specified range
    
    Args:
        min: Minimum value (inclusive)
        max: Maximum value (inclusive)
        count: Number of random integers to generate
    
    Returns:
        
    """
    arguments = {
        "min": min,
        "max": max,
        "count": count
    }
    
    return call_api("1777316659559427", "generate_random_integer", arguments)

def generate_random_float(
    min: Optional[float] = 0.0,
    max: Optional[float] = 1.0,
    count: Optional[int] = 1.0,
    precision: Optional[int] = 6.0
) -> Dict[str, Any]:
    """
    Generate cryptographically secure random floating-point numbers
    
    Args:
        min: Minimum value (inclusive)
        max: Maximum value (exclusive)
        count: Number of random floats to generate
        precision: Number of decimal places to round to
    
    Returns:
        
    """
    arguments = {
        "min": min,
        "max": max,
        "count": count,
        "precision": precision
    }
    
    return call_api("1777316659559427", "generate_random_float", arguments)

def generate_random_bytes(
    length: Optional[int] = 32.0,
    encoding: Optional[str] = "hex"
) -> Dict[str, Any]:
    """
    Generate cryptographically secure random bytes
    
    Args:
        length: Number of random bytes to generate
        encoding: Output encoding format
    
    Returns:
        
    """
    arguments = {
        "length": length,
        "encoding": encoding
    }
    
    return call_api("1777316659559427", "generate_random_bytes", arguments)

def generate_uuid(
    count: Optional[int] = 1.0,
    format: Optional[str] = "standard"
) -> Dict[str, Any]:
    """
    Generate a cryptographically secure UUID (v4)
    
    Args:
        count: Number of UUIDs to generate
        format: UUID format
    
    Returns:
        
    """
    arguments = {
        "count": count,
        "format": format
    }
    
    return call_api("1777316659559427", "generate_uuid", arguments)

def generate_random_string(
    length: Optional[int] = 16.0,
    charset: Optional[str] = "alphanumeric",
    count: Optional[int] = 1.0
) -> Dict[str, Any]:
    """
    Generate a cryptographically secure random string
    
    Args:
        length: Length of the random string
        charset: Character set to use
        count: Number of random strings to generate
    
    Returns:
        
    """
    arguments = {
        "length": length,
        "charset": charset,
        "count": count
    }
    
    return call_api("1777316659559427", "generate_random_string", arguments)

def generate_random_choice(
    choices: null,
    count: Optional[int] = 1.0,
    allow_duplicates: Optional[bool] = True
) -> Dict[str, Any]:
    """
    Randomly select items from a given list using cryptographically secure randomness
    
    Args:
        choices: Array of items to choose from
        count: Number of items to select
        allow_duplicates: Whether to allow duplicate selections
    
    Returns:
        
    """
    arguments = {
        "choices": choices,
        "count": count,
        "allow_duplicates": allow_duplicates
    }
    
    return call_api("1777316659559427", "generate_random_choice", arguments)

def generate_random_boolean(
    count: Optional[int] = 1.0,
    probability: Optional[float] = 0.5
) -> Dict[str, Any]:
    """
    Generate cryptographically secure random boolean values
    
    Args:
        count: Number of random booleans to generate
        probability: Probability of true (0.0 to 1.0)
    
    Returns:
        
    """
    arguments = {
        "count": count,
        "probability": probability
    }
    
    return call_api("1777316659559427", "generate_random_boolean", arguments)

