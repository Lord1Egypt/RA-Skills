from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def remember_memory(
    category: str,
    data: str,
    tags: Optional[null] = [],
    is_global: bool
) -> Dict[str, Any]:
    """
    Stores a memory with optional tags in a specified category
    
    Args:
        category: The category to store the memory in
        data: The data to store in memory
        tags: Optional tags for categorizing the memory
        is_global: Whether to store in global or local memory
    
    Returns:
        
    """
    arguments = {
        "category": category,
        "data": data,
        "tags": tags,
        "is_global": is_global
    }
    
    return call_api("1777316659460099", "remember_memory", arguments)

def retrieve_memories(
    category: str,
    is_global: bool
) -> Dict[str, Any]:
    """
    Retrieves all memories from a specified category
    
    Args:
        category: The category to retrieve memories from, use '*' for all categories
        is_global: Whether to retrieve from global or local memory
    
    Returns:
        
    """
    arguments = {
        "category": category,
        "is_global": is_global
    }
    
    return call_api("1777316659460099", "retrieve_memories", arguments)

def remove_memory_category(
    category: str,
    is_global: bool
) -> Dict[str, Any]:
    """
    Removes all memories within a specified category
    
    Args:
        category: The category to remove, use '*' for all categories
        is_global: Whether to remove from global or local memory
    
    Returns:
        
    """
    arguments = {
        "category": category,
        "is_global": is_global
    }
    
    return call_api("1777316659460099", "remove_memory_category", arguments)

def remove_specific_memory(
    category: str,
    memory_content: str,
    is_global: bool
) -> Dict[str, Any]:
    """
    Removes a specific memory within a specified category
    
    Args:
        category: The category containing the memory to remove
        memory_content: Content of the memory to remove (partial match)
        is_global: Whether to remove from global or local memory
    
    Returns:
        
    """
    arguments = {
        "category": category,
        "memory_content": memory_content,
        "is_global": is_global
    }
    
    return call_api("1777316659460099", "remove_specific_memory", arguments)

