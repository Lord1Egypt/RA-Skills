from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def daniels_calculate_vdot(
    distance: float,
    time: float
) -> Dict[str, Any]:
    """
    Calculate VDOT according to Jack Daniels.

Args:
    distance: Distance in meters.
    time: Time in seconds.

Returns:
    dict:
        vdot (float): The calculated VDOT value, representing the runner's aerobic capacity based on the input distance and time.
    
    Args:
        distance: null
        time: null
    
    Returns:
        null
    """
    arguments = {
        "distance": distance,
        "time": time
    }
    
    return call_api("1777419068722179", "daniels_calculate_vdot", arguments)

def daniels_calculate_training_paces(
    vdot: float
) -> Dict[str, Any]:
    """
    Get recommended training paces for a given VDOT, based on Jack Daniels' formulas.

Args:
    vdot: VDOT value.

Returns:
    dict:
        easy (dict): Recommended easy pace range with lower and upper bounds.
        marathon (dict): Recommended marathon pace with value and format.
        threshold (dict): Recommended threshold pace with value and format.
        interval (dict): Recommended interval pace with value and format.
        repetition (dict): Recommended repetition pace with value and format.
    
    Args:
        vdot: null
    
    Returns:
        null
    """
    arguments = {
        "vdot": vdot
    }
    
    return call_api("1777419068722179", "daniels_calculate_training_paces", arguments)

def daniels_predict_race_time(
    current_distance: float,
    current_time: float,
    target_distance: float
) -> Dict[str, Any]:
    """
    Predict race time for a target distance based on a current race performance.
Uses Jack Daniels' equivalent performance methodology.

Args:
    current_distance: Distance of known performance in meters.
    current_time: Time of known performance in seconds.
    target_distance: Distance for race time prediction in meters.

Returns:
    dict: Daniels' VDOT method prediction with value, format, and time_seconds.
    
    Args:
        current_distance: null
        current_time: null
        target_distance: null
    
    Returns:
        null
    """
    arguments = {
        "current_distance": current_distance,
        "current_time": current_time,
        "target_distance": target_distance
    }
    
    return call_api("1777419068722179", "daniels_predict_race_time", arguments)

def riegel_predict_race_time(
    current_distance: float,
    current_time: float,
    target_distance: float
) -> Dict[str, Any]:
    """
    Predict race time for a target distance based on a current race performance.
Uses Riegel's formula.

Args:
    current_distance: Distance of known performance in meters.
    current_time: Time of known performance in seconds.
    target_distance: Distance for race time prediction in meters.

Returns:
    dict: Riegel's formula prediction with value, format, and time_seconds.
    
    Args:
        current_distance: null
        current_time: null
        target_distance: null
    
    Returns:
        null
    """
    arguments = {
        "current_distance": current_distance,
        "current_time": current_time,
        "target_distance": target_distance
    }
    
    return call_api("1777419068722179", "riegel_predict_race_time", arguments)

def mcmillan_calculate_velocity_markers(
    distance: float,
    time: float
) -> Dict[str, Any]:
    """
    Calculate velocity markers (vLT, CV, vVO2) from a race performance using McMillan methodology.

Args:
    distance: Race distance in meters
    time: Race time in seconds

Returns:
    Dictionary containing velocity markers with paces in MM:SS/km format
    
    Args:
        distance: null
        time: null
    
    Returns:
        null
    """
    arguments = {
        "distance": distance,
        "time": time
    }
    
    return call_api("1777419068722179", "mcmillan_calculate_velocity_markers", arguments)

def mcmillan_predict_race_times(
    distance: float,
    time: float
) -> Dict[str, Any]:
    """
    Predict race times for standard distances based on a single race performance using McMillan methodology.

Args:
    distance: Race distance in meters
    time: Race time in seconds

Returns:
    Dictionary containing predicted race times in HH:MM:SS format
    
    Args:
        distance: null
        time: null
    
    Returns:
        null
    """
    arguments = {
        "distance": distance,
        "time": time
    }
    
    return call_api("1777419068722179", "mcmillan_predict_race_times", arguments)

def mcmillan_calculate_training_paces(
    distance: float,
    time: float
) -> Dict[str, Any]:
    """
    Calculate training paces for all zones based on a race performance using McMillan methodology.

Args:
    distance: Race distance in meters
    time: Race time in seconds

Returns:
    Dictionary containing training paces organized by zones (endurance, stamina, speed, sprint)
    
    Args:
        distance: null
        time: null
    
    Returns:
        null
    """
    arguments = {
        "distance": distance,
        "time": time
    }
    
    return call_api("1777419068722179", "mcmillan_calculate_training_paces", arguments)

def mcmillan_heart_rate_zones(
    age: int,
    resting_heart_rate: int,
    max_heart_rate: Optional[int] = None
) -> Dict[str, Any]:
    """
    Calculate heart rate training zones based on age, resting heart rate, and optional max heart rate.
Uses McMillan methodology with multiple max HR estimation formulas and both HRMAX and HRRESERVE methods.

Args:
    age: Runner's age in years
    resting_heart_rate: Resting heart rate in BPM
    max_heart_rate: Optional maximum heart rate in BPM (if None, will be estimated)

Returns:
    Dictionary containing estimated max HR, effective max HR, and training zones with both HRMAX and HRRESERVE calculations
    
    Args:
        age: null
        resting_heart_rate: null
        max_heart_rate: null
    
    Returns:
        null
    """
    arguments = {
        "age": age,
        "resting_heart_rate": resting_heart_rate,
        "max_heart_rate": max_heart_rate
    }
    
    return call_api("1777419068722179", "mcmillan_heart_rate_zones", arguments)

def convert_pace(
    value: float,
    from_unit: str,
    to_unit: str
) -> Dict[str, Any]:
    """
    Convert between different pace and speed units.

Args:
    value: The numeric value to convert.
    from_unit: Source unit ("min_km", "min_mile", "kmh", "mph").
    to_unit: Target unit ("min_km", "min_mile", "kmh", "mph").

Returns:
    dict:
        value (float): Converted numeric value.
        formatted (str): Human-readable formatted result.
        unit (str): Target unit descriptor.

Raises:
    ValueError: If from_unit or to_unit are not valid, or if conversion is not supported.
    
    Args:
        value: null
        from_unit: null
        to_unit: null
    
    Returns:
        null
    """
    arguments = {
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit
    }
    
    return call_api("1777419068722179", "convert_pace", arguments)

