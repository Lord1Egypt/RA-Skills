from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_street_level_crimes(
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    poly: Optional[str] = None,
    date: Optional[str] = None,
    category: Optional[str] = "all-crime"
) -> Dict[str, Any]:
    """
    Retrieve street-level crimes by lat/lng or custom polygon area
    
    Args:
        lat: Latitude of the requested crime area
        lng: Longitude of the requested crime area
        poly: The lat/lng pairs defining the boundary of the custom area
        date: Limit results to a specific month (YYYY-MM)
        category: The crime category
    
    Returns:
        
    """
    arguments = {
        "lat": lat,
        "lng": lng,
        "poly": poly,
        "date": date,
        "category": category
    }
    
    return call_api("1777316659577859", "get_street_level_crimes", arguments)

def get_street_level_outcomes(
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    poly: Optional[str] = None,
    location_id: Optional[float] = None,
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve outcomes by lat/lng, custom polygon, or location ID
    
    Args:
        lat: Latitude of the requested area
        lng: Longitude of the requested area
        poly: The lat/lng pairs defining the boundary of the custom area
        location_id: The ID of the location
        date: Limit results to a specific month (YYYY-MM)
    
    Returns:
        
    """
    arguments = {
        "lat": lat,
        "lng": lng,
        "poly": poly,
        "location_id": location_id,
        "date": date
    }
    
    return call_api("1777316659577859", "get_street_level_outcomes", arguments)

def get_crimes_at_location(
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    location_id: Optional[float] = None,
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve crimes at a specific location by ID or nearest to lat/lng
    
    Args:
        lat: Latitude of the requested crime area
        lng: Longitude of the requested crime area
        location_id: The ID of the location
        date: Limit results to a specific month (YYYY-MM)
    
    Returns:
        
    """
    arguments = {
        "lat": lat,
        "lng": lng,
        "location_id": location_id,
        "date": date
    }
    
    return call_api("1777316659577859", "get_crimes_at_location", arguments)

def get_crimes_no_location(
    category: str,
    force: str,
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve crimes that could not be mapped to a location
    
    Args:
        category: The category of the crimes
        force: Specific police force
        date: Limit results to a specific month (YYYY-MM)
    
    Returns:
        
    """
    arguments = {
        "category": category,
        "force": force,
        "date": date
    }
    
    return call_api("1777316659577859", "get_crimes_no_location", arguments)

def get_crime_categories(
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve valid crime categories for a given date
    
    Args:
        date: Specific month (YYYY-MM)
    
    Returns:
        
    """
    arguments = {
        "date": date
    }
    
    return call_api("1777316659577859", "get_crime_categories", arguments)

def get_last_updated(
) -> Dict[str, Any]:
    """
    Retrieve the date when crime data was last updated
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659577859", "get_last_updated", arguments)

def get_outcomes_for_crime(
    persistent_id: str
) -> Dict[str, Any]:
    """
    Retrieve outcomes for a specific crime by persistent ID
    
    Args:
        persistent_id: The 64-character unique identifier for the crime
    
    Returns:
        
    """
    arguments = {
        "persistent_id": persistent_id
    }
    
    return call_api("1777316659577859", "get_outcomes_for_crime", arguments)

def get_list_of_forces(
) -> Dict[str, Any]:
    """
    Retrieve a list of all police forces
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659577859", "get_list_of_forces", arguments)

def get_force_details(
    force_id: str
) -> Dict[str, Any]:
    """
    Retrieve details for a specific police force
    
    Args:
        force_id: The unique identifier for the force
    
    Returns:
        
    """
    arguments = {
        "force_id": force_id
    }
    
    return call_api("1777316659577859", "get_force_details", arguments)

def get_senior_officers(
    force_id: str
) -> Dict[str, Any]:
    """
    Retrieve senior officers for a specific police force
    
    Args:
        force_id: The unique identifier for the force
    
    Returns:
        
    """
    arguments = {
        "force_id": force_id
    }
    
    return call_api("1777316659577859", "get_senior_officers", arguments)

def get_neighbourhoods(
    force_id: str
) -> Dict[str, Any]:
    """
    Retrieve a list of neighbourhoods for a specific police force
    
    Args:
        force_id: The unique identifier for the force
    
    Returns:
        
    """
    arguments = {
        "force_id": force_id
    }
    
    return call_api("1777316659577859", "get_neighbourhoods", arguments)

def get_neighbourhood_details(
    force_id: str,
    neighbourhood_id: str
) -> Dict[str, Any]:
    """
    Retrieve details for a specific neighbourhood within a force
    
    Args:
        force_id: The unique identifier for the force
        neighbourhood_id: The unique identifier for the neighbourhood
    
    Returns:
        
    """
    arguments = {
        "force_id": force_id,
        "neighbourhood_id": neighbourhood_id
    }
    
    return call_api("1777316659577859", "get_neighbourhood_details", arguments)

def get_neighbourhood_boundary(
    force_id: str,
    neighbourhood_id: str
) -> Dict[str, Any]:
    """
    Retrieve the boundary coordinates for a specific neighbourhood
    
    Args:
        force_id: The unique identifier for the force
        neighbourhood_id: The unique identifier for the neighbourhood
    
    Returns:
        
    """
    arguments = {
        "force_id": force_id,
        "neighbourhood_id": neighbourhood_id
    }
    
    return call_api("1777316659577859", "get_neighbourhood_boundary", arguments)

def get_neighbourhood_team(
    force_id: str,
    neighbourhood_id: str
) -> Dict[str, Any]:
    """
    Retrieve the team members for a specific neighbourhood
    
    Args:
        force_id: The unique identifier for the force
        neighbourhood_id: The unique identifier for the neighbourhood
    
    Returns:
        
    """
    arguments = {
        "force_id": force_id,
        "neighbourhood_id": neighbourhood_id
    }
    
    return call_api("1777316659577859", "get_neighbourhood_team", arguments)

def get_neighbourhood_events(
    force_id: str,
    neighbourhood_id: str
) -> Dict[str, Any]:
    """
    Retrieve events scheduled for a specific neighbourhood
    
    Args:
        force_id: The unique identifier for the force
        neighbourhood_id: The unique identifier for the neighbourhood
    
    Returns:
        
    """
    arguments = {
        "force_id": force_id,
        "neighbourhood_id": neighbourhood_id
    }
    
    return call_api("1777316659577859", "get_neighbourhood_events", arguments)

def get_neighbourhood_priorities(
    force_id: str,
    neighbourhood_id: str
) -> Dict[str, Any]:
    """
    Retrieve policing priorities for a specific neighbourhood
    
    Args:
        force_id: The unique identifier for the force
        neighbourhood_id: The unique identifier for the neighbourhood
    
    Returns:
        
    """
    arguments = {
        "force_id": force_id,
        "neighbourhood_id": neighbourhood_id
    }
    
    return call_api("1777316659577859", "get_neighbourhood_priorities", arguments)

def locate_neighbourhood(
    lat: float,
    lng: float
) -> Dict[str, Any]:
    """
    Find the neighbourhood policing team for a given latitude and longitude
    
    Args:
        lat: Latitude of the location
        lng: Longitude of the location
    
    Returns:
        
    """
    arguments = {
        "lat": lat,
        "lng": lng
    }
    
    return call_api("1777316659577859", "locate_neighbourhood", arguments)

def get_stop_searches_by_area(
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    poly: Optional[str] = None,
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve stop and searches within a 1-mile radius or custom area
    
    Args:
        lat: Latitude of the centre point
        lng: Longitude of the centre point
        poly: Lat/lng pairs defining a polygon
        date: Specific month (YYYY-MM)
    
    Returns:
        
    """
    arguments = {
        "lat": lat,
        "lng": lng,
        "poly": poly,
        "date": date
    }
    
    return call_api("1777316659577859", "get_stop_searches_by_area", arguments)

def get_stop_searches_by_location(
    location_id: float,
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve stop and searches at a specific location by ID
    
    Args:
        location_id: The ID of the location
        date: Specific month (YYYY-MM)
    
    Returns:
        
    """
    arguments = {
        "location_id": location_id,
        "date": date
    }
    
    return call_api("1777316659577859", "get_stop_searches_by_location", arguments)

def get_stop_searches_no_location(
    force_id: str,
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve stop and searches that could not be mapped to a location
    
    Args:
        force_id: The unique identifier for the force
        date: Specific month (YYYY-MM)
    
    Returns:
        
    """
    arguments = {
        "force_id": force_id,
        "date": date
    }
    
    return call_api("1777316659577859", "get_stop_searches_no_location", arguments)

def get_stop_searches_by_force(
    force_id: str,
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve stop and searches reported by a specific force
    
    Args:
        force_id: The unique identifier for the force
        date: Specific month (YYYY-MM)
    
    Returns:
        
    """
    arguments = {
        "force_id": force_id,
        "date": date
    }
    
    return call_api("1777316659577859", "get_stop_searches_by_force", arguments)

