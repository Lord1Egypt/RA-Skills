from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def list_departments(
) -> Dict[str, Any]:
    """
    List all departments in the Metropolitan Museum of Art (Met Museum)
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1815966663015434", "list_departments", arguments)

def search_museum_objects(
    q: str,
    departmentId: Optional[int] = None,
    pageSize: Optional[int] = None,
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    Search for objects in the Metropolitan Museum of Art (Met Museum). Will return Total objects found, followed by a paginated list of Object Ids. Use page and pageSize to paginate results.
    
    Args:
        q: The search query, Returns a listing of all Object IDs for objects that contain the search query within the object's data
        departmentId: Returns objects that are in the specified department. The departmentId should come from the 'list-departments' tool.
        pageSize: Number of object IDs to return per page (max 100)
        page: 1-based page number for paginated object IDs
    
    Returns:
        
    """
    arguments = {
        "q": q,
        "departmentId": departmentId,
        "pageSize": pageSize,
        "page": page
    }
    
    return call_api("1815966663015434", "search_museum_objects", arguments)

def get_museum_object(
    objectId: int
) -> Dict[str, Any]:
    """
    Get a museum object by its ID, from the Metropolitan Museum of Art Collection. Use this when the user asks for deeper details on a specific object ID.
    
    Args:
        objectId: The positive integer ID of the museum object to retrieve.
    
    Returns:
        
    """
    arguments = {
        "objectId": objectId
    }
    
    return call_api("1815966663015434", "get_museum_object", arguments)

