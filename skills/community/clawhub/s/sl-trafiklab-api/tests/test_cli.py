import pytest
from unittest.mock import patch, MagicMock
import os
import json
import sys
from datetime import datetime, timedelta

# Import cli code
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import scripts.cli as cli


@pytest.fixture
def prefs_path(tmp_path):
    """Fixture returning a temp file path for preferences."""
    return str(tmp_path / "preferences.json")


def test_load_prefs_empty(prefs_path):
    """Should load default dictionary when file doesn't exist."""
    prefs = cli.load_prefs(prefs_path)
    assert prefs == {"favourite_stops": [], "favourite_routes": []}


def test_save_and_load_prefs(prefs_path):
    """Should save and correctly reload preferences."""
    sample = {
        "favourite_stops": [{"id": 9999, "name": "Test Site"}],
        "favourite_routes": []
    }
    cli.save_prefs(sample, prefs_path)
    loaded = cli.load_prefs(prefs_path)
    assert loaded["favourite_stops"][0]["id"] == 9999
    assert loaded["favourite_stops"][0]["name"] == "Test Site"


def test_save_site_to_favorites(prefs_path):
    """Should add a site to favorites."""
    args = MagicMock()
    args.preferences = prefs_path
    args.site_id = "1234"
    args.name = "My Stop"
    args.lines = "10,20"
    args.modes = "bus,metro"

    cli.cmd_site_save(args)
    prefs = cli.load_prefs(prefs_path)
    assert len(prefs["favourite_stops"]) == 1
    
    stop = prefs["favourite_stops"][0]
    assert stop["id"] == 1234
    assert stop["name"] == "My Stop"
    assert stop["lines"] == ["10", "20"]
    assert stop["transport_modes"] == ["BUS", "METRO"]


def test_remove_site_from_favorites(prefs_path):
    """Should remove a site from favorites."""
    prefs = {
        "favourite_stops": [{"id": 1234, "name": "Stop A"}],
        "favourite_routes": []
    }
    cli.save_prefs(prefs, prefs_path)

    args = MagicMock()
    args.preferences = prefs_path
    args.site_id = "1234"

    cli.cmd_site_remove(args)
    prefs = cli.load_prefs(prefs_path)
    assert len(prefs["favourite_stops"]) == 0


@patch('scripts.cli.make_request')
def test_site_check_single_and_all(mock_make_request, prefs_path):
    """Should fetch status for one or all stops."""
    prefs = {
        "favourite_stops": [
            {"id": 1111, "name": "Stop One", "lines": ["10"], "transport_modes": ["BUS"]},
            {"id": 2222, "name": "Stop Two"}
        ],
        "favourite_routes": []
    }
    cli.save_prefs(prefs, prefs_path)

    def mock_api(url, params=None):
        if "messages" in url:
            return [{
                "id": "D1",
                "message_variants": [{"header": "Disruption here"}]
            }]
        elif "departures" in url:
            return {
                "departures": [{
                    "line": {"designation": "10"},
                    "destination": "Destination",
                    "scheduled": "2026-06-30T12:00:00",
                    "expected": "2026-06-30T12:00:00",
                    "state": "CANCELLED"
                }]
            }
        return {}

    mock_make_request.side_effect = mock_api

    # 1. Check all stops
    args = MagicMock()
    args.preferences = prefs_path
    args.site_id = None
    args.verbose = True

    with patch('sys.stdout.write') as mock_stdout:
        cli.cmd_site_check(args)
        written_calls = "".join(call[0][0] for call in mock_stdout.call_args_list)
        assert "Checking all favorite sites..." in written_calls
        assert "Status: WARNING" in written_calls
        assert "Disruption at Stop One" in written_calls
        assert "Canceled: Line 10 to Destination" in written_calls

    # 2. Check single stop
    args.site_id = "2222"
    with patch('sys.stdout.write') as mock_stdout:
        cli.cmd_site_check(args)
        written_calls = "".join(call[0][0] for call in mock_stdout.call_args_list)
        assert "Checking site Stop Two..." in written_calls


@patch('scripts.cli.make_request')
def test_route_check_tight_connection_warning(mock_make_request, prefs_path):
    """Should raise tight connection warning if buffer < 5 minutes."""
    route = {
        "name": "Commute Route",
        "legs": [
            {
                "lines": ["10"],
                "from": {"id": 1, "name": "Site A"},
                "to": {"id": 2, "name": "Site B"},
                "travel_time_minutes": 10
            },
            {
                "lines": ["20"],
                "from": {"id": 2, "name": "Site B"},
                "to": {"id": 3, "name": "Site C"}
            }
        ]
    }
    cli.save_prefs({"favourite_stops": [], "favourite_routes": [route]}, prefs_path)

    now = datetime.now()
    dep1_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
    dep2_time = now.replace(hour=8, minute=13, second=0, microsecond=0)

    def mock_api(url, params=None):
        if "sites/1/departures" in url:
            return {
                "departures": [{
                    "line": {"designation": "10"},
                    "destination": "Site B",
                    "scheduled": dep1_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "expected": dep1_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "state": "EXPECTED"
                }]
            }
        elif "sites/2/departures" in url:
            return {
                "departures": [{
                    "line": {"designation": "20"},
                    "destination": "Site C",
                    "scheduled": dep2_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "expected": dep2_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "state": "EXPECTED"
                }]
            }
        return {}

    mock_make_request.side_effect = mock_api

    args = MagicMock()
    args.preferences = prefs_path
    args.alias = None
    args.verbose = False

    with patch('sys.stdout.write') as mock_stdout:
        cli.cmd_route_check(args)
        written_calls = "".join(call[0][0] for call in mock_stdout.call_args_list)
        assert "Warnings:" in written_calls
        assert "Tight connection" in written_calls
        assert "has only 3 min buffer" in written_calls


@patch('scripts.cli.make_request')
def test_route_check_with_direction_filtering_and_sequential_filtering(mock_make_request, prefs_path):
    """Verify that direction list filtering and sequential arrival filtering works in route check."""
    route = {
      "name": "Commute Route",
      "legs": [
        {
          "lines": ["10"],
          "from": { "id": 1386, "name": "Stop A" },
          "to": { "id": 1339, "name": "Station B" },
          "travel_time_minutes": 7
        },
        {
          "lines": ["40", "41"],
          "from": { "id": 9530, "name": "Station B" },
          "to": { "id": 9526, "name": "Stop C" },
          "travel_time_minutes": 14,
          "direction": ["Terminus B", "Terminus C"]
        }
      ]
    }
    cli.save_prefs({"favourite_stops": [], "favourite_routes": [route]}, prefs_path)

    now = datetime.now()
    bus_dep = now.replace(hour=8, minute=0, second=0, microsecond=0)
    
    # Leg 2 options:
    # 1. Terminus A (wrong direction, arrives 08:10)
    # 2. Terminus B (right direction, arrives 08:05 - before bus arrives at 08:07 - should be filtered sequentially)
    # 3. Terminus C (right direction, arrives 08:11 - valid connection)
    train_uppsala = now.replace(hour=8, minute=10, second=0, microsecond=0)
    train_tumba_early = now.replace(hour=8, minute=5, second=0, microsecond=0)
    train_sodertalje = now.replace(hour=8, minute=11, second=0, microsecond=0)

    def mock_api(url, params=None):
        if "sites/1386/departures" in url:
            return {
                "departures": [{
                    "line": {"designation": "10"},
                    "destination": "Destination A",
                    "scheduled": bus_dep.strftime("%Y-%m-%dT%H:%M:%S"),
                    "expected": bus_dep.strftime("%Y-%m-%dT%H:%M:%S"),
                    "state": "EXPECTED"
                }]
            }
        elif "sites/9530/departures" in url:
            return {
                "departures": [
                    {
                        "line": {"designation": "40"},
                        "destination": "Terminus A",
                        "direction": "Terminus A",
                        "direction_code": 1,
                        "scheduled": train_uppsala.strftime("%Y-%m-%dT%H:%M:%S"),
                        "expected": train_uppsala.strftime("%Y-%m-%dT%H:%M:%S"),
                        "state": "EXPECTED"
                    },
                    {
                        "line": {"designation": "40"},
                        "destination": "Terminus B",
                        "direction": "Terminus B",
                        "direction_code": 2,
                        "scheduled": train_tumba_early.strftime("%Y-%m-%dT%H:%M:%S"),
                        "expected": train_tumba_early.strftime("%Y-%m-%dT%H:%M:%S"),
                        "state": "EXPECTED"
                    },
                    {
                        "line": {"designation": "41"},
                        "destination": "Terminus C",
                        "direction": "Terminus C",
                        "direction_code": 2,
                        "scheduled": train_sodertalje.strftime("%Y-%m-%dT%H:%M:%S"),
                        "expected": train_sodertalje.strftime("%Y-%m-%dT%H:%M:%S"),
                        "state": "EXPECTED"
                    }
                ]
            }
        return {}

    mock_make_request.side_effect = mock_api

    args = MagicMock()
    args.preferences = prefs_path
    args.alias = "Commute Route"
    args.verbose = False

    with patch('sys.stdout.write') as mock_stdout:
        cli.cmd_route_check(args)
        written_calls = "".join(call[0][0] for call in mock_stdout.call_args_list)
        
        # Verify departures printing
        assert "Leg 1: Line 10 from Stop A to Station B" in written_calls
        assert "08:00 -> ~08:07" in written_calls
        assert "Leg 2: Line 40, 41 (toward Terminus B, Terminus C) from Station B to Stop C" in written_calls
        
        # Terminus C should be listed (valid connection >= 08:07 and correct direction)
        assert "08:11 -> ~08:25" in written_calls
        
        # Terminus A (wrong direction) and Terminus B early (before arrival time 08:07) should NOT be listed
        assert "Terminus A" not in written_calls
        assert "08:05 (Terminus B)" not in written_calls
        
        # Verify tight connection message contents
        assert "Warnings:" in written_calls
        assert "leaving Stop A at 08:00" in written_calls
        assert "toward Terminus C departing at 08:11" in written_calls
        assert "has only 4 min buffer" in written_calls


@patch('scripts.cli.make_request')
def test_route_find_alias_matching(mock_make_request, prefs_path):
    # Favorite route setup
    route = {
        "name": "commute",
        "legs": [
            {
                "lines": ["10"],
                "from": {"id": 18001001, "name": "Stop A"},
                "to": {"id": 18001002, "name": "Stop B"}
            },
            {
                "lines": ["40"],
                "from": {"id": 18001002, "name": "Stop B"},
                "to": {"id": 18001003, "name": "Stop C"}
            }
        ]
    }
    cli.save_prefs({"favourite_stops": [], "favourite_routes": [route]}, prefs_path)

    def mock_api(url, params=None):
        if "stop-finder" in url:
            name = params["name_sf"]
            return {
                "locations": [{
                    "id": "909100100000" + name,
                    "name": name,
                    "properties": {"stopId": name if name.startswith("1800") else "1800" + name}
                }]
            }
        elif "trips" in url:
            return {
                "journeys": [
                    {
                        "tripDuration": 1200,
                        "interchanges": 1,
                        "legs": [
                            {
                                "transportation": {"disassembledName": "10"},
                                "origin": {"parent": {"name": "Stop A", "properties": {"stopId": "18001001"}}},
                                "destination": {"parent": {"name": "Stop B", "properties": {"stopId": "18001002"}}},
                                "duration": 600
                            },
                            {
                                "transportation": {"disassembledName": "40"},
                                "origin": {"parent": {"name": "Stop B", "properties": {"stopId": "18001002"}}},
                                "destination": {"parent": {"name": "Stop C", "properties": {"stopId": "18001003"}}},
                                "duration": 600
                            }
                        ]
                    },
                    {
                        "tripDuration": 1500,
                        "interchanges": 1,
                        "legs": [
                            {
                                "transportation": {"disassembledName": "10"},
                                "origin": {"parent": {"name": "Stop A", "properties": {"stopId": "18001001"}}},
                                "destination": {"parent": {"name": "Stop B", "properties": {"stopId": "18001002"}}},
                                "duration": 600
                            },
                            {
                                "transportation": {"disassembledName": "99"},
                                "origin": {"parent": {"name": "Stop B", "properties": {"stopId": "18001002"}}},
                                "destination": {"parent": {"name": "Stop C", "properties": {"stopId": "18001003"}}},
                                "duration": 900
                            }
                        ]
                    }
                ]
            }
        return {}

    mock_make_request.side_effect = mock_api

    args = MagicMock()
    args.preferences = prefs_path
    args.origin_or_alias = "commute"
    args.destination = None
    args.all = False
    args.time = None
    args.date = None
    args.number = 3

    with patch('sys.stdout.write') as mock_stdout:
        cli.cmd_route_find(args)
        written_calls = "".join(call[0][0] for call in mock_stdout.call_args_list)
        assert "Option 1: Total duration 20 min" in written_calls
        assert "Line 10 from Stop A to Stop B" in written_calls
        assert "Line 40 from Stop B to Stop C" in written_calls
        assert "Option 2" not in written_calls


@patch('scripts.cli.make_request')
def test_route_find_all_flag(mock_make_request, prefs_path):
    route = {
        "name": "commute",
        "legs": [
            {
                "lines": ["10"],
                "from": {"id": 18001001, "name": "Stop A"},
                "to": {"id": 18001002, "name": "Stop B"}
            }
        ]
    }
    cli.save_prefs({"favourite_stops": [], "favourite_routes": [route]}, prefs_path)

    def mock_api(url, params=None):
        if "stop-finder" in url:
            name = params["name_sf"]
            return {
                "locations": [{
                    "id": "909100100000" + name,
                    "name": name,
                    "properties": {"stopId": name if name.startswith("1800") else "1800" + name}
                }]
            }
        elif "trips" in url:
            return {
                "journeys": [
                    {
                        "tripDuration": 600,
                        "interchanges": 0,
                        "legs": [
                            {
                                "transportation": {"disassembledName": "10"},
                                "origin": {"parent": {"name": "Stop A", "properties": {"stopId": "18001001"}}},
                                "destination": {"parent": {"name": "Stop B", "properties": {"stopId": "18001002"}}},
                                "duration": 600
                            }
                        ]
                    },
                    {
                        "tripDuration": 900,
                        "interchanges": 0,
                        "legs": [
                            {
                                "transportation": {"disassembledName": "99"},
                                "origin": {"parent": {"name": "Stop A", "properties": {"stopId": "18001001"}}},
                                "destination": {"parent": {"name": "Stop B", "properties": {"stopId": "18001002"}}},
                                "duration": 900
                            }
                        ]
                    }
                ]
            }
        return {}

    mock_make_request.side_effect = mock_api

    args = MagicMock()
    args.preferences = prefs_path
    args.origin_or_alias = "commute"
    args.destination = None
    args.all = True
    args.time = None
    args.date = None
    args.number = 3

    with patch('sys.stdout.write') as mock_stdout:
        cli.cmd_route_find(args)
        written_calls = "".join(call[0][0] for call in mock_stdout.call_args_list)
        assert "Option 1: Total duration 10 min" in written_calls
        assert "Option 2: Total duration 15 min" in written_calls


@patch('scripts.cli.make_request')
def test_route_find_mismatch_feedback(mock_make_request, prefs_path):
    route = {
        "name": "commute",
        "legs": [
            {
                "lines": ["999"],
                "from": {"id": 18001001, "name": "Stop A"},
                "to": {"id": 18001002, "name": "Stop B"}
            }
        ]
    }
    cli.save_prefs({"favourite_stops": [], "favourite_routes": [route]}, prefs_path)

    def mock_api(url, params=None):
        if "stop-finder" in url:
            name = params["name_sf"]
            return {
                "locations": [{
                    "id": "909100100000" + name,
                    "name": name,
                    "properties": {"stopId": name if name.startswith("1800") else "1800" + name}
                }]
            }
        elif "trips" in url:
            return {
                "journeys": [
                    {
                        "tripDuration": 600,
                        "interchanges": 0,
                        "legs": [
                            {
                                "transportation": {"disassembledName": "10"},
                                "origin": {"parent": {"name": "Stop A", "properties": {"stopId": "18001001"}}},
                                "destination": {"parent": {"name": "Stop B", "properties": {"stopId": "18001002"}}},
                                "duration": 600
                            }
                        ]
                    }
                ]
            }
        return {}

    mock_make_request.side_effect = mock_api

    args = MagicMock()
    args.preferences = prefs_path
    args.origin_or_alias = "commute"
    args.destination = None
    args.all = False
    args.time = None
    args.date = None
    args.number = 3

    with patch('sys.stdout.write') as mock_stdout:
        cli.cmd_route_find(args)
        written_calls = "".join(call[0][0] for call in mock_stdout.call_args_list)
        assert "No journey options matched your saved route leg preferences (e.g. Line 999 from Stop A)." in written_calls
        assert "SL returned 1 alternative route proposals. Run with '--all' to display them." in written_calls


@patch('scripts.cli.make_request')
def test_route_save_dynamic_and_unconstrained(mock_make_request, prefs_path):
    def mock_api(url, params=None):
        if "stop-finder" in url:
            name = params["name_sf"]
            return {
                "locations": [{
                    "id": "909100100000" + name,
                    "name": name,
                    "properties": {"stopId": name if name.startswith("1800") else "1800" + name}
                }]
            }
        elif "trips" in url:
            return {
                "journeys": [
                    {
                        "tripDuration": 600,
                        "interchanges": 0,
                        "legs": [
                            {
                                "transportation": {"disassembledName": "10"},
                                "origin": {"parent": {"name": "Stop A", "properties": {"stopId": "18001001"}}},
                                "destination": {"parent": {"name": "Stop B", "properties": {"stopId": "18001002"}}},
                                "duration": 600
                            }
                        ]
                    }
                ]
            }
        return {}

    mock_make_request.side_effect = mock_api

    # 1. Test Dynamic Proposal Save (Option 1)
    args = MagicMock()
    args.preferences = prefs_path
    args.args = ["1001", "1002", "1", "dynamic-commute"]

    with patch('sys.stdout.write') as mock_stdout:
        cli.cmd_route_save(args)
        
    prefs = cli.load_prefs(prefs_path)
    saved_routes = prefs.get("favourite_routes", [])
    target = next((r for r in saved_routes if r["name"] == "dynamic-commute"), None)
    assert target is not None
    assert len(target["legs"]) == 1
    assert target["legs"][0]["lines"] == ["10"]
    assert target["legs"][0]["from"]["id"] == 1001
    assert target["legs"][0]["to"]["id"] == 1002
    assert target["legs"][0]["from"]["stop_id"] == 1001
    assert target["legs"][0]["to"]["stop_id"] == 1002

    # 2. Test Unconstrained Save (Option 0 - augmented with duration and lines)
    args.args = ["1001", "1002", "0", "unconstrained-commute"]
    with patch('sys.stdout.write') as mock_stdout:
        cli.cmd_route_save(args)

    prefs = cli.load_prefs(prefs_path)
    saved_routes = prefs.get("favourite_routes", [])
    target = next((r for r in saved_routes if r["name"] == "unconstrained-commute"), None)
    assert target is not None
    assert len(target["legs"]) == 1
    assert target["legs"][0]["lines"] == ["10"]
    assert target["legs"][0]["travel_time_minutes"] == 10
    assert target["legs"][0]["from"]["id"] == 1001
    assert target["legs"][0]["to"]["id"] == 1002

    # 3. Test 3-argument syntax (equivalent to option 0)
    args.args = ["1001", "1002", "three-args-commute"]
    with patch('sys.stdout.write') as mock_stdout:
        cli.cmd_route_save(args)

    prefs = cli.load_prefs(prefs_path)
    saved_routes = prefs.get("favourite_routes", [])
    target = next((r for r in saved_routes if r["name"] == "three-args-commute"), None)
    assert target is not None
    assert len(target["legs"]) == 1
    assert target["legs"][0]["lines"] == ["10"]
    assert target["legs"][0]["travel_time_minutes"] == 10
    assert target["legs"][0]["from"]["id"] == 1001
    assert target["legs"][0]["to"]["id"] == 1002

    # 4. Test fallback to unconstrained default (when API returns no journeys)
    def mock_api_empty(url, params=None):
        if "stop-finder" in url:
            name = params["name_sf"]
            return {
                "locations": [{
                    "id": "909100100000" + name,
                    "name": name,
                    "properties": {"stopId": name if name.startswith("1800") else "1800" + name}
                }]
            }
        return {} # Returns no journeys/trips
    
    mock_make_request.side_effect = mock_api_empty
    args.args = ["1001", "1002", "fallback-commute"]
    with patch('sys.stdout.write') as mock_stdout:
        cli.cmd_route_save(args)

    prefs = cli.load_prefs(prefs_path)
    saved_routes = prefs.get("favourite_routes", [])
    target = next((r for r in saved_routes if r["name"] == "fallback-commute"), None)
    assert target is not None
    assert len(target["legs"]) == 1
    assert target["legs"][0]["lines"] == []
    assert target["legs"][0]["travel_time_minutes"] == 0
    assert target["legs"][0]["from"]["id"] == 1001
    assert target["legs"][0]["to"]["id"] == 1002


@patch('scripts.cli.make_request')
def test_route_save_time_and_date_flags(mock_make_request, prefs_path):
    called_params = []
    def mock_api(url, params=None):
        if "stop-finder" in url:
            name = params["name_sf"]
            return {
                "locations": [{
                    "id": "909100100000" + name,
                    "name": name,
                    "properties": {"stopId": "1800" + name}
                }]
            }
        elif "trips" in url:
            called_params.append(params)
            return {
                "journeys": [
                    {
                        "tripDuration": 600,
                        "interchanges": 0,
                        "legs": [
                            {
                                "transportation": {"disassembledName": "10"},
                                "origin": {"parent": {"name": "Stop A", "properties": {"stopId": "18001001"}}},
                                "destination": {"parent": {"name": "Stop B", "properties": {"stopId": "18001002"}}},
                                "duration": 600
                            }
                        ]
                    }
                ]
            }
        return {}

    mock_make_request.side_effect = mock_api

    args = MagicMock()
    args.preferences = prefs_path
    args.args = ["1001", "1002", "1", "time-commute"]
    args.time = "08:30"
    args.date = "2026-07-02"

    with patch('sys.stdout.write'):
        cli.cmd_route_save(args)

    assert len(called_params) == 1
    assert called_params[0]["itd_time"] == "0830"
    assert called_params[0]["itd_date"] == "20260702"


@patch('scripts.cli.make_request')
def test_route_save_consolidates_lines(mock_make_request, prefs_path):
    def mock_api(url, params=None):
        if "stop-finder" in url:
            name = params["name_sf"]
            return {
                "locations": [{
                    "id": "909100100000" + name,
                    "name": name,
                    "properties": {"stopId": "1800" + name}
                }]
            }
        elif "trips" in url:
            return {
                "journeys": [
                    {
                        "tripDuration": 600,
                        "interchanges": 0,
                        "legs": [
                            {
                                "transportation": {"disassembledName": "10"},
                                "origin": {"parent": {"name": "Stop A", "properties": {"stopId": "18001001"}}},
                                "destination": {"parent": {"name": "Stop B", "properties": {"stopId": "18001002"}}},
                                "duration": 600
                            }
                        ]
                    },
                    {
                        "tripDuration": 650,
                        "interchanges": 0,
                        "legs": [
                            {
                                "transportation": {"disassembledName": "20"},
                                "origin": {"parent": {"name": "Stop A", "properties": {"stopId": "18001001"}}},
                                "destination": {"parent": {"name": "Stop B", "properties": {"stopId": "18001002"}}},
                                "duration": 650
                            }
                        ]
                    }
                ]
            }
        return {}

    mock_make_request.side_effect = mock_api

    args = MagicMock()
    args.preferences = prefs_path
    args.args = ["1001", "1002", "1", "consolidated-commute"]
    args.time = None
    args.date = None

    with patch('sys.stdout.write'):
        cli.cmd_route_save(args)

    prefs = cli.load_prefs(prefs_path)
    saved_routes = prefs.get("favourite_routes", [])
    target = next((r for r in saved_routes if r["name"] == "consolidated-commute"), None)
    assert target is not None
    assert len(target["legs"]) == 1
    assert target["legs"][0]["lines"] == ["10", "20"]
    assert target["legs"][0]["from"]["id"] == 1001
    assert target["legs"][0]["to"]["id"] == 1002


@patch('scripts.cli.make_request')
def test_route_find_with_via_and_not_via(mock_make_request, prefs_path):
    cli.save_prefs({"favourite_stops": [], "favourite_routes": []}, prefs_path)

    def mock_api(url, params=None):
        if "stop-finder" in url:
            name = params["name_sf"]
            return {
                "locations": [{
                    "id": "1800" + name,
                    "name": name,
                    "properties": {"stopId": "1800" + name}
                }]
            }
        elif "trips" in url:
            return {
                "journeys": [
                    {
                        "tripDuration": 600,
                        "interchanges": 0,
                        "legs": [
                            {
                                "transportation": {"disassembledName": "10"},
                                "origin": {"parent": {"name": "Stop A", "properties": {"stopId": "18001001"}}},
                                "destination": {"parent": {"name": "Stop B", "properties": {"stopId": "18001002"}}},
                                "duration": 600
                            }
                        ]
                    }
                ]
            }
        return {}

    mock_make_request.side_effect = mock_api

    args = MagicMock()
    args.preferences = prefs_path
    args.origin_or_alias = "Stop A"
    args.destination = "Stop B"
    args.all = False
    args.time = None
    args.date = None
    args.number = 3
    args.via = "Stop V"
    args.dwell_time = "00:15"
    args.not_via = "Stop N"

    with patch('sys.stdout.write'):
        cli.cmd_route_find(args)

    trips_call = next(call for call in mock_make_request.call_args_list if "trips" in call[0][0])
    trips_params = trips_call[0][1]
    assert trips_params["type_via"] == "any"
    assert trips_params["name_via"] == "1800Stop V"
    assert trips_params["dwell_time"] == "0015"
    assert trips_params["type_not_via"] == "any"
    assert trips_params["name_not_via"] == "1800Stop N"


@patch('scripts.cli.make_request')
def test_route_find_dwell_time_requires_via(mock_make_request, prefs_path):
    cli.save_prefs({"favourite_stops": [], "favourite_routes": []}, prefs_path)

    def mock_api(url, params=None):
        if "stop-finder" in url:
            name = params["name_sf"]
            return {
                "locations": [{
                    "id": "1800" + name,
                    "name": name,
                    "properties": {"stopId": "1800" + name}
                }]
            }
        return {}
    mock_make_request.side_effect = mock_api

    args = MagicMock()
    args.preferences = prefs_path
    args.origin_or_alias = "Stop A"
    args.destination = "Stop B"
    args.all = False
    args.time = None
    args.date = None
    args.number = 3
    args.via = None
    args.dwell_time = "00:15"
    args.not_via = None

    with pytest.raises(SystemExit) as excinfo:
        cli.cmd_route_find(args)
    assert excinfo.value.code == 1


@patch('scripts.cli.make_request')
def test_route_find_unresolved_via(mock_make_request, prefs_path):
    cli.save_prefs({"favourite_stops": [], "favourite_routes": []}, prefs_path)

    def mock_api(url, params=None):
        if "stop-finder" in url:
            name = params["name_sf"]
            if name == "Stop V":
                return {}
            return {
                "locations": [{
                    "id": "1800" + name,
                    "name": name,
                    "properties": {"stopId": "1800" + name}
                }]
            }
        return {}
    mock_make_request.side_effect = mock_api

    args = MagicMock()
    args.preferences = prefs_path
    args.origin_or_alias = "Stop A"
    args.destination = "Stop B"
    args.all = False
    args.time = None
    args.date = None
    args.number = 3
    args.via = "Stop V"
    args.dwell_time = None
    args.not_via = None

    with pytest.raises(SystemExit) as excinfo:
        cli.cmd_route_find(args)
    assert excinfo.value.code == 1






@patch('scripts.cli.make_request')
def test_site_departures_filtered_locally_not_capped(mock_make_request, tmp_path):
    """--line/--direction should be filtered client-side so the response is not
    truncated to the API's ~3-row server-side cap for filtered queries.

    The mock mimics the real API: a filtered request (with line/direction params)
    returns a small subset, while an unfiltered request returns the full board.
    The command must fetch the unfiltered board and filter locally, returning all
    matching departures rather than the capped subset.
    """
    full_board = {
        "departures": [
            {"line": {"designation": "5"}, "direction_code": 1, "destination": "East", "scheduled": "2026-08-17T08:00:00", "expected": "2026-08-17T08:00:00", "state": "EXPECTED"},
            {"line": {"designation": "5"}, "direction_code": 1, "destination": "East", "scheduled": "2026-08-17T08:13:00", "expected": "2026-08-17T08:13:00", "state": "EXPECTED"},
            {"line": {"designation": "5"}, "direction_code": 2, "destination": "West", "scheduled": "2026-08-17T08:10:00", "expected": "2026-08-17T08:10:00", "state": "EXPECTED"},
            {"line": {"designation": "7"}, "direction_code": 1, "destination": "East", "scheduled": "2026-08-17T08:05:00", "expected": "2026-08-17T08:05:00", "state": "EXPECTED"},
            {"line": {"designation": "5"}, "direction_code": 1, "destination": "East", "scheduled": "2026-08-17T08:18:00", "expected": "2026-08-17T08:18:00", "state": "EXPECTED"},
        ]
    }

    def mock_api(url, params=None):
        # Mimic the real server-side cap for filtered queries.
        if params and (params.get("line") or params.get("direction")):
            return {"departures": full_board["departures"][:3]}
        return full_board

    mock_make_request.side_effect = mock_api

    args = MagicMock()
    args.site_id = "9117"
    args.line = "5"
    args.direction = 1
    args.transport = None
    args.forecast = None

    with patch('sys.stdout.write') as mock_stdout:
        cli.cmd_site_departures(args)
        written = "".join(call[0][0] for call in mock_stdout.call_args_list)

    # Must return ALL line-5 direction-1 departures (3), not the capped subset.
    assert "08:00" in written
    assert "08:13" in written
    assert "08:18" in written
    # Line 7 and the opposite-direction (direction 2) departure must be filtered out.
    assert "08:05" not in written
    assert "West" not in written
