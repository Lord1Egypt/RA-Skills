import pytest
import sys
import os

# Import cli code
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import scripts.cli as cli


@pytest.mark.integration
def test_live_site_list_api():
    """Verify the sites API is reachable and returns stop data."""
    url = f"{cli.TRANSPORT_API_URL}/sites"
    data = cli.make_request(url)
    
    assert data is not None
    assert isinstance(data, list)
    assert len(data) > 0
    
    first_item = data[0]
    assert "id" in first_item
    assert "name" in first_item
    assert isinstance(first_item["id"], int)


@pytest.mark.integration
def test_live_departures_api():
    """Verify the departures API is active and returns data for T-Centralen (9001)."""
    site_id = 9001
    url = f"{cli.TRANSPORT_API_URL}/sites/{site_id}/departures"
    data = cli.make_request(url, {"forecast": 30})
    
    assert data is not None
    assert "departures" in data
    assert isinstance(data["departures"], list)


@pytest.mark.integration
def test_live_deviations_api():
    """Verify the deviations API is active and returns data (even if empty)."""
    url = f"{cli.DEVIATIONS_API_URL}/messages"
    data = cli.make_request(url, {"future": False})
    
    assert data is not None
    assert isinstance(data, list)
    if len(data) > 0:
        first_dev = data[0]
        assert "id" in first_dev or "deviation_case_id" in first_dev
        assert "message_variants" in first_dev


@pytest.mark.integration
def test_live_stop_finder_api():
    """Verify stop finder API returns location results for a stop search."""
    url = f"{cli.JOURNEY_API_URL}/stop-finder"
    data = cli.make_request(url, {
        "name_sf": "odenplan",
        "any_obj_filter_sf": 2,
        "type_sf": "any"
    })
    
    assert data is not None
    assert "locations" in data
    assert isinstance(data["locations"], list)
    assert len(data["locations"]) > 0
    assert "id" in data["locations"][0]


@pytest.mark.integration
def test_live_trips_api():
    """Verify trips API calculates journey proposals between two site points."""
    url = f"{cli.JOURNEY_API_URL}/trips"
    data = cli.make_request(url, {
        "type_origin": "any",
        "name_origin": "9091001000009117",
        "type_destination": "any",
        "name_destination": "9091001000009001",
        "calc_number_of_trips": 1
    })
    
    assert data is not None
    assert "journeys" in data
    assert isinstance(data["journeys"], list)
    assert len(data["journeys"]) > 0
    assert "legs" in data["journeys"][0]
