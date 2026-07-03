from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def random_int(
    low: int,
    high: int
) -> Dict[str, Any]:
    """
    Generate a random integer between low and high (inclusive).

Args:
    low: Lower bound (inclusive)
    high: Upper bound (inclusive)

Returns:
    Random integer between low and high
    
    Args:
        low: null
        high: null
    
    Returns:
        null
    """
    arguments = {
        "low": low,
        "high": high
    }
    
    return call_api("1777419067540483", "random_int", arguments)

def random_float(
    low: Optional[float] = 0.0,
    high: Optional[float] = 1.0
) -> Dict[str, Any]:
    """
    Generate a random float between low and high.

Args:
    low: Lower bound (default 0.0)
    high: Upper bound (default 1.0)

Returns:
    Random float between low and high
    
    Args:
        low: null
        high: null
    
    Returns:
        null
    """
    arguments = {
        "low": low,
        "high": high
    }
    
    return call_api("1777419067540483", "random_float", arguments)

def random_choices(
    population: null,
    k: Optional[int] = 1.0,
    weights: Optional[null] = None
) -> Dict[str, Any]:
    """
    Choose k items from population with replacement, optionally weighted.

Args:
    population: List of items to choose from
    k: Number of items to choose (default 1)
    weights: Optional weights for each item (default None for equal weights)

Returns:
    List of k chosen items
    
    Args:
        population: null
        k: null
        weights: null
    
    Returns:
        null
    """
    arguments = {
        "population": population,
        "k": k,
        "weights": weights
    }
    
    return call_api("1777419067540483", "random_choices", arguments)

def random_shuffle(
    items: null
) -> Dict[str, Any]:
    """
    Return a new list with items in random order.

Args:
    items: List of items to shuffle

Returns:
    New list with items in random order
    
    Args:
        items: null
    
    Returns:
        null
    """
    arguments = {
        "items": items
    }
    
    return call_api("1777419067540483", "random_shuffle", arguments)

def random_sample(
    population: null,
    k: int
) -> Dict[str, Any]:
    """
    Choose k unique items from population without replacement.

Args:
    population: List of items to choose from
    k: Number of items to choose

Returns:
    List of k unique chosen items
    
    Args:
        population: null
        k: null
    
    Returns:
        null
    """
    arguments = {
        "population": population,
        "k": k
    }
    
    return call_api("1777419067540483", "random_sample", arguments)

def secure_token_hex(
    nbytes: Optional[int] = 32.0
) -> Dict[str, Any]:
    """
    Generate a secure random hex token.

Args:
    nbytes: Number of random bytes to generate (default 32)

Returns:
    Hex string containing 2*nbytes characters
    
    Args:
        nbytes: null
    
    Returns:
        null
    """
    arguments = {
        "nbytes": nbytes
    }
    
    return call_api("1777419067540483", "secure_token_hex", arguments)

def secure_random_int(
    upper_bound: int
) -> Dict[str, Any]:
    """
    Generate a secure random integer below upper_bound.

Args:
    upper_bound: Upper bound (exclusive)

Returns:
    Random integer in range [0, upper_bound)
    
    Args:
        upper_bound: null
    
    Returns:
        null
    """
    arguments = {
        "upper_bound": upper_bound
    }
    
    return call_api("1777419067540483", "secure_random_int", arguments)

