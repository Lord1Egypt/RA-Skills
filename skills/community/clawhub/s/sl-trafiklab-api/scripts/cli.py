#!/usr/bin/env python3
"""
CLI wrapper for the SL Trafiklab API.
Provides site search, departures, deviations, favorite management, and autonomous monitoring.
Zero dependencies: uses only Python standard libraries.
"""

import argparse
import sys
import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta, timezone


def get_stockholm_now():
    """Get the current datetime in Europe/Stockholm timezone, zero-dependency."""
    utc_now = datetime.now(timezone.utc).replace(tzinfo=None)
    year = utc_now.year
    
    # CEST starts last Sunday of March at 01:00 UTC
    march_31 = datetime(year, 3, 31, 1, 0, 0)
    march_transition = march_31 - timedelta(days=(march_31.weekday() + 1) % 7)
    
    # CEST ends last Sunday of October at 01:00 UTC
    oct_31 = datetime(year, 10, 31, 1, 0, 0)
    oct_transition = oct_31 - timedelta(days=(oct_31.weekday() + 1) % 7)
    
    if march_transition <= utc_now < oct_transition:
        return utc_now + timedelta(hours=2) # UTC+2 (CEST)
    else:
        return utc_now + timedelta(hours=1) # UTC+1 (CET)
TRANSPORT_API_URL = "https://transport.integration.sl.se/v1"
DEVIATIONS_API_URL = "https://deviations.integration.sl.se/v1"


def make_request(url, params=None):
    """Perform HTTP GET request and return parsed JSON."""
    if params:
        # Filter out None values and handle lists/iterables for doseq
        filtered_params = {}
        for k, v in params.items():
            if v is not None:
                if isinstance(v, bool):
                    filtered_params[k] = str(v).lower()
                else:
                    filtered_params[k] = v
        url = f"{url}?{urllib.parse.urlencode(filtered_params, doseq=True)}"

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "OpenClaw-SL-Trafiklab/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        sys.stderr.write(f"Error fetching data from API: {e}\n")
        return None


# =====================================================================
# Preference Helpers
# =====================================================================

def get_prefs_path(path=None):
    """Retrieve preferences path, defaulting to .sl/preferences.json in CWD."""
    if path:
        return path
    return os.path.join(os.getcwd(), ".sl", "preferences.json")


def load_prefs(path=None):
    """Load configuration from preferences file."""
    p = get_prefs_path(path)
    if not os.path.exists(p):
        return {"favourite_stops": [], "favourite_routes": []}
    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure keys exist
            if "favourite_stops" not in data:
                data["favourite_stops"] = []
            if "favourite_routes" not in data:
                data["favourite_routes"] = []
            return data
    except Exception:
        return {"favourite_stops": [], "favourite_routes": []}


def save_prefs(prefs, path=None):
    """Save configuration to preferences file."""
    p = get_prefs_path(path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(prefs, f, indent=2, ensure_ascii=False)


# Journey Planner API
JOURNEY_API_URL = "https://journeyplanner.integration.sl.se/v2"


def resolve_stop(query):
    """Resolve a stop name or ID using SL Journey Planner stop-finder."""
    query_str = str(query).strip()
    if len(query_str) == 4 and query_str.isdigit():
        query_str = "1800" + query_str

    url = f"{JOURNEY_API_URL}/stop-finder"
    res = make_request(url, {
        "name_sf": query_str,
        "any_obj_filter_sf": 2,
        "type_sf": "any"
    })
    if not res or not res.get("locations"):
        return None
    
    # Return best match if found, else first item
    best = None
    for loc in res["locations"]:
        if loc.get("isBest"):
            best = loc
            break
    if not best:
        best = res["locations"][0]
    return best


def extract_site_id(loc_node):
    """Extract stop ID from platform or stop area location node."""
    if not loc_node:
        return ""
    props = loc_node.get("parent", {}).get("properties", {})
    stop_id = props.get("stopId")
    if not stop_id:
        props = loc_node.get("properties", {})
        stop_id = props.get("stopId")
    if not stop_id:
        full_id = loc_node.get("parent", {}).get("id") or loc_node.get("id") or ""
        if len(full_id) >= 8:
            stop_id = full_id[-8:]
        else:
            stop_id = full_id
    
    # Strip "1800" prefix from parent site IDs
    if stop_id and stop_id.startswith("1800") and len(stop_id) > 4:
        stop_id = stop_id[4:]
        
    return stop_id


def extract_stop_name(loc_node):
    """Extract and clean stop name from location node."""
    if not loc_node:
        return ""
    
    parent = loc_node.get("parent", {})
    name = None
    if parent and parent.get("type") != "locality":
        name = parent.get("disassembledName") or parent.get("name")
        
    if not name:
        name = loc_node.get("disassembledName")
    if not name:
        name = loc_node.get("name")
        
    if name:
        if name.startswith("Stockholm, "):
            name = name[len("Stockholm, "):]
        if name.endswith(", Stockholm"):
            name = name[:-len(", Stockholm")]
    return name or ""


def clean_compare_name(name):
    """Normalize station names by stripping locality suffixes and parenthetical details for robust matching."""
    if not name:
        return ""
    name = str(name).strip()
    if name.startswith("Stockholm, "):
        name = name[len("Stockholm, "):]
    if name.endswith(", Stockholm"):
        name = name[:-len(", Stockholm")]
    # Strip parenthetical parts like "(på Swedenborgsgatan)" or "(Rosenlundsg)"
    import re
    name = re.sub(r"\s*\(.*\)", "", name)
    return name.strip().lower()


def is_walk_leg(leg):
    """Check if a trip leg is a walking or transfer footpath."""
    if not leg:
        return True
    if "transportation" not in leg:
        return True
    prod_name = leg.get("transportation", {}).get("product", {}).get("name", "").lower()
    if prod_name in ("footpath", "transfer", "walk"):
        return True
    if not leg.get("transportation", {}).get("number") and not leg.get("transportation", {}).get("disassembledName"):
        return True
    return False


# =====================================================================
# CLI Commands implementation
# =====================================================================

def cmd_site_list(args):
    """List/Search sites matching query term."""
    url = f"{TRANSPORT_API_URL}/sites"
    sys.stdout.write("Fetching site list...\n")
    data = make_request(url)
    if not data:
        sys.exit(1)

    query = args.query.lower()
    matches = []
    for item in data:
        name = item.get("name", "")
        if query in name.lower():
            matches.append({
                "id": item.get("id"),
                "name": name
            })

    if not matches:
        sys.stdout.write(f"No sites found matching '{args.query}'.\n")
        return

    sys.stdout.write(f"Found {len(matches)} matching sites (showing top {args.limit}):\n")
    for m in matches[:args.limit]:
        sys.stdout.write(f"- {m['id']}: {m['name']}\n")


def cmd_site_departures(args):
    """Fetch departures for a specific site ID.

    The SL transport departures API truncates FILTERED responses server-side to a
    small subset (~3 rows for a line+direction filter), regardless of requested
    limits. To return the full per-line set within the API's lookahead window, we
    fetch the unfiltered board (transport/forecast are still passed through) and
    apply the line/direction filters locally instead.
    """
    url = f"{TRANSPORT_API_URL}/sites/{args.site_id}/departures"
    params = {
        # line/direction filters are deliberately NOT sent to the API: sending
        # them truncates the response to ~3 rows. We filter locally below.
        "transport": args.transport,
        "forecast": args.forecast
    }
    data = make_request(url, params)
    if not data:
        sys.exit(1)

    departures = data.get("departures", [])
    # Apply line/direction filters client-side to avoid the API's server-side cap.
    if args.line:
        line_str = str(args.line)
        departures = [d for d in departures
                      if str(d.get("line", {}).get("designation")) == line_str]
    if args.direction is not None:
        departures = [d for d in departures
                      if d.get("direction_code") == args.direction]
    if not departures:
        sys.stdout.write("No upcoming departures found.\n")
        return

    sys.stdout.write(f"Departures for site {args.site_id}:\n")
    header = f"{'Line':<6} {'Destination':<22} {'Expected/Scheduled':<24} {'State'}"
    sys.stdout.write(header + "\n" + "-" * len(header) + "\n")
    for dep in departures:
        line = dep.get("line", {}).get("designation", "")
        dest = dep.get("destination", "")
        sched = dep.get("scheduled", "")
        expected = dep.get("expected", sched)
        state = dep.get("state", "EXPECTED")

        # Format departure time display
        time_str = expected
        if dep.get("display"):
            time_str = f"{dep.get('display')} ({expected})"

        sys.stdout.write(f"{line:<6} {dest:<22} {time_str:<24} {state}\n")


def cmd_deviations(args):
    """Fetch deviations generally or filtered by site/line."""
    url = f"{DEVIATIONS_API_URL}/messages"
    params = {
        "future": args.future,
        "site": args.site,
        "line": args.line
    }
    data = make_request(url, params)
    if data is None:
        sys.exit(1)

    if not data:
        sys.stdout.write("No active deviations found.\n")
        return

    sys.stdout.write(f"Active deviations ({len(data)}):\n")
    for item in data:
        dev_id = item.get("id") or item.get("deviation_case_id")
        variants = item.get("message_variants", [])
        header = "No header available"
        details = ""
        if variants:
            header = variants[0].get("header", header)
            details = variants[0].get("details", "")

        sys.stdout.write(f"\n[{dev_id}] {header}\n")
        if args.verbose and details:
            sys.stdout.write(f"Details: {details}\n")


def cmd_site_save(args):
    """Save favorite site."""
    prefs = load_prefs(args.preferences)
    stops = prefs.get("favourite_stops", [])
    site_id = int(args.site_id)

    # Filter out existing to prevent duplicates
    stops = [s for s in stops if s.get("id") != site_id]

    entry = {"id": site_id, "name": args.name}
    if args.lines:
        entry["lines"] = [l.strip() for l in args.lines.split(",")]
    if args.modes:
        entry["transport_modes"] = [m.strip().upper() for m in args.modes.split(",")]

    stops.append(entry)
    prefs["favourite_stops"] = stops
    save_prefs(prefs, args.preferences)
    sys.stdout.write(f"Successfully added favorite site: {args.name} ({site_id})\n")


def cmd_site_remove(args):
    """Remove favorite site."""
    prefs = load_prefs(args.preferences)
    stops = prefs.get("favourite_stops", [])
    site_id = int(args.site_id)

    filtered = [s for s in stops if s.get("id") != site_id]
    if len(stops) == len(filtered):
        sys.stdout.write(f"Site ID {site_id} not found in favorites.\n")
        return

    prefs["favourite_stops"] = filtered
    save_prefs(prefs, args.preferences)
    sys.stdout.write(f"Successfully removed favorite site: {site_id}\n")


def cmd_route_find(args):
    """Find travel proposals dynamically using SL Journey Planner."""
    prefs = load_prefs(args.preferences)
    routes = prefs.get("favourite_routes", [])

    origin_name = None
    dest_name = None
    saved_route = None

    # Determine if origin_or_alias refers to a saved alias
    for r in routes:
        if r.get("name") == args.origin_or_alias:
            saved_route = r
            break

    if saved_route:
        # Load from saved route legs
        legs = saved_route.get("legs", [])
        if not legs:
            sys.stderr.write(f"Saved route '{args.origin_or_alias}' has no configured legs.\n")
            sys.exit(1)
        origin_name = str(legs[0]["from"]["id"])
        dest_name = str(legs[-1]["to"]["id"])
    else:
        # Require destination if not using a saved alias
        if not args.destination:
            sys.stderr.write("Error: destination is required when origin_or_alias is not a saved route alias.\n")
            sys.exit(1)
        origin_name = args.origin_or_alias
        dest_name = args.destination

    # Resolve origin and destination to locations
    origin_stop = resolve_stop(origin_name)
    if not origin_stop:
        sys.stderr.write(f"Could not resolve origin stop: {origin_name}\n")
        sys.exit(1)
    
    dest_stop = resolve_stop(dest_name)
    if not dest_stop:
        sys.stderr.write(f"Could not resolve destination stop: {dest_name}\n")
        sys.exit(1)

    # Safely extract and resolve via & not-via optional stops (handling Mock environments)
    via_arg = getattr(args, "via", None)
    via_val = via_arg if isinstance(via_arg, (str, int)) else None

    dwell_arg = getattr(args, "dwell_time", None)
    dwell_val = dwell_arg if isinstance(dwell_arg, (str, int)) else None

    not_via_arg = getattr(args, "not_via", None)
    not_via_val = not_via_arg if isinstance(not_via_arg, (str, int)) else None

    via_stop = None
    if via_val:
        via_stop = resolve_stop(via_val)
        if not via_stop:
            sys.stderr.write(f"Could not resolve via stop: {via_val}\n")
            sys.exit(1)

    not_via_stop = None
    if not_via_val:
        not_via_stop = resolve_stop(not_via_val)
        if not not_via_stop:
            sys.stderr.write(f"Could not resolve not-via stop: {not_via_val}\n")
            sys.exit(1)

    url = f"{JOURNEY_API_URL}/trips"
    params = {
        "type_origin": "any",
        "name_origin": origin_stop.get("id"),
        "type_destination": "any",
        "name_destination": dest_stop.get("id"),
        "calc_number_of_trips": args.number
    }
    if args.time:
        params["itd_time"] = args.time.replace(":", "")
    if args.date:
        params["itd_date"] = args.date.replace("-", "")

    if via_stop:
        params["type_via"] = "any"
        params["name_via"] = via_stop.get("id")
        if dwell_val:
            params["dwell_time"] = str(dwell_val).replace(":", "")
    elif dwell_val:
        sys.stderr.write("Error: --dwell-time requires --via to be specified.\n")
        sys.exit(1)

    if not_via_stop:
        params["type_not_via"] = "any"
        params["name_not_via"] = not_via_stop.get("id")

    res = make_request(url, params)
    if not res or not res.get("journeys"):
        sys.stdout.write("No travel proposals found.\n")
        return

    journeys = res.get("journeys", [])
    displayed_journeys = []
    
    # Leg preference filtering
    if saved_route and not args.all:
        saved_legs = saved_route.get("legs", [])
        # Check if saved route is unconstrained (1 leg, no line list)
        is_unconstrained = len(saved_legs) == 1 and not saved_legs[0].get("lines")
        
        if is_unconstrained:
            displayed_journeys = journeys
        else:
            for j in journeys:
                # Filter out walking legs for matching
                transit_legs = [leg for leg in j.get("legs", []) if not is_walk_leg(leg)]
                if len(transit_legs) != len(saved_legs):
                    continue
                
                match = True
                for idx, s_leg in enumerate(saved_legs):
                    p_leg = transit_legs[idx]
                    
                    # 1. Match line designation
                    line_desig = p_leg.get("transportation", {}).get("disassembledName")
                    lines_str = [str(x) for x in s_leg.get("lines", [])]
                    if not line_desig or str(line_desig) not in lines_str:
                        match = False
                        break
                    
                    # 2. Match origin site ID & Name
                    o_id = extract_site_id(p_leg.get("origin"))
                    s_from_id = str(s_leg.get("from", {}).get("id"))
                    s_from_stop_id = str(s_leg.get("from", {}).get("stop_id", s_from_id))
                    
                    id_matched = o_id and (o_id.endswith(s_from_id) or s_from_id.endswith(o_id) or o_id == s_from_stop_id)
                    if not id_matched:
                        # Fallback to Cleaned Name Equality
                        p_name = extract_stop_name(p_leg.get("origin"))
                        s_name = s_leg.get("from", {}).get("name", "")
                        if clean_compare_name(p_name) != clean_compare_name(s_name):
                            match = False
                            break
                    
                    # 3. Match destination site ID & Name
                    d_id = extract_site_id(p_leg.get("destination"))
                    s_to_id = str(s_leg.get("to", {}).get("id"))
                    s_to_stop_id = str(s_leg.get("to", {}).get("stop_id", s_to_id))
                    
                    id_matched = d_id and (d_id.endswith(s_to_id) or s_to_id.endswith(d_id) or d_id == s_to_stop_id)
                    if not id_matched:
                        # Fallback to Cleaned Name Equality
                        p_name = extract_stop_name(p_leg.get("destination"))
                        s_name = s_leg.get("to", {}).get("name", "")
                        if clean_compare_name(p_name) != clean_compare_name(s_name):
                            match = False
                            break
                
                if match:
                    displayed_journeys.append(j)
                    
            if not displayed_journeys:
                # Get the sample/first line and first origin for mismatch message
                eg_line = saved_legs[0].get("lines", [""])[0]
                eg_from = saved_legs[0].get("from", {}).get("name", "")
                sys.stdout.write(f"No journey options matched your saved route leg preferences (e.g. Line {eg_line} from {eg_from}).\n")
                sys.stdout.write(f"SL returned {len(journeys)} alternative route proposals. Run with '--all' to display them.\n")
                return
    else:
        displayed_journeys = journeys

    # Output proposals
    for idx, journey in enumerate(displayed_journeys):
        duration = journey.get("tripRtDuration") or journey.get("tripDuration") or 0
        duration_mins = int(duration / 60)
        interchanges = journey.get("interchanges", 0)
        
        sys.stdout.write(f"\nOption {idx + 1}: Total duration {duration_mins} min ({interchanges} changes)\n")
        
        transit_leg_idx = 1
        for leg in journey.get("legs", []):
            origin_name = extract_stop_name(leg.get("origin"))
            dest_name = extract_stop_name(leg.get("destination"))
            
            dep_time = parse_time(leg.get("origin", {}).get("departureTimeEstimated") or leg.get("origin", {}).get("departureTimePlanned"))
            arr_time = parse_time(leg.get("destination", {}).get("arrivalTimeEstimated") or leg.get("destination", {}).get("arrivalTimePlanned"))
            dep_str = dep_time.strftime("%H:%M") if dep_time else ""
            arr_str = arr_time.strftime("%H:%M") if arr_time else ""
            
            if is_walk_leg(leg):
                # Walk leg
                leg_duration = int((leg.get("duration") or 0) / 60)
                sys.stdout.write(f"  Walk: {origin_name} to {dest_name} ({leg_duration} min)\n")
            else:
                line = leg.get("transportation", {}).get("disassembledName")
                direction = leg.get("transportation", {}).get("destination", {}).get("name")
                dir_suffix = f" (toward {direction})" if direction else ""
                sys.stdout.write(f"  Leg {transit_leg_idx}: Line {line}{dir_suffix} from {origin_name} to {dest_name}\n")
                sys.stdout.write(f"    - {dep_str} -> {arr_str}\n")
                transit_leg_idx += 1


def cmd_route_save(args):
    """Save favorite route."""
    prefs = load_prefs(args.preferences)
    routes = prefs.get("favourite_routes", [])

    if len(args.args) == 2:
        name = args.args[0]
        legs_json = args.args[1]
        try:
            legs = json.loads(legs_json)
            if not isinstance(legs, list):
                raise ValueError("Legs must be a JSON array of leg objects.")
        except Exception as e:
            sys.stderr.write(f"Invalid legs JSON: {e}\n")
            sys.exit(1)
    elif len(args.args) in (3, 4):
        origin = args.args[0]
        destination = args.args[1]
        if len(args.args) == 3:
            proposal_index = 0
            name = args.args[2]
        else:
            try:
                proposal_index = int(args.args[2])
            except ValueError:
                sys.stderr.write("Proposal index must be an integer.\n")
                sys.exit(1)
            name = args.args[3]

        # Resolve origin and destination stops
        origin_stop = resolve_stop(origin)
        if not origin_stop:
            sys.stderr.write(f"Could not resolve origin stop: {origin}\n")
            sys.exit(1)
        dest_stop = resolve_stop(destination)
        if not dest_stop:
            sys.stderr.write(f"Could not resolve destination stop: {destination}\n")
            sys.exit(1)

        resolved_stops_cache = {}
        def get_resolved_parent_id(stop_node):
            if not stop_node:
                return 0
            stop_name = stop_node.get("name")
            if not stop_name:
                stop_id_str = extract_site_id(stop_node)
                return int(stop_id_str) if (stop_id_str and stop_id_str.isdigit()) else 0
            
            if stop_name in resolved_stops_cache:
                return resolved_stops_cache[stop_name]
            
            resolved = resolve_stop(stop_name)
            resolved_id_str = extract_site_id(resolved)
            resolved_id = int(resolved_id_str) if (resolved_id_str and resolved_id_str.isdigit()) else 0
            if not resolved_id:
                stop_id_str = extract_site_id(stop_node)
                resolved_id = int(stop_id_str) if (stop_id_str and stop_id_str.isdigit()) else 0
            
            resolved_stops_cache[stop_name] = resolved_id
            return resolved_id

        if proposal_index == 0:
            # Save unconstrained direct start/stop connection
            o_id_str = extract_site_id(origin_stop)
            o_id = int(o_id_str) if o_id_str else 0
            o_name = extract_stop_name(origin_stop)
            d_id_str = extract_site_id(dest_stop)
            d_id = int(d_id_str) if d_id_str else 0
            d_name = extract_stop_name(dest_stop)
            
            legs = [{
                "lines": [],
                "from": {"id": o_id, "name": o_name},
                "to": {"id": d_id, "name": d_name},
                "travel_time_minutes": 0
            }]

            # Try to query trips to get travel duration and line information
            o_location_id = origin_stop.get("id")
            d_location_id = dest_stop.get("id")
            url = f"{JOURNEY_API_URL}/trips"
            params = {
                "type_origin": "any",
                "name_origin": o_location_id,
                "type_destination": "any",
                "name_destination": d_location_id,
                "calc_number_of_trips": 3
            }
            if getattr(args, "time", None):
                params["itd_time"] = args.time.replace(":", "")
            if getattr(args, "date", None):
                params["itd_date"] = args.date.replace("-", "")

            res = make_request(url, params)
            if res and res.get("journeys"):
                journeys = res.get("journeys", [])
                if journeys:
                    # 1. Use the duration of the first option as the travel time
                    first_journey = journeys[0]
                    duration = first_journey.get("tripRtDuration") or first_journey.get("tripDuration") or 0
                    duration_mins = int(duration / 60)
                    legs[0]["travel_time_minutes"] = duration_mins

                    # 2. Consolidate lines and directions of the first transit leg across all journey options
                    lines_set = set()
                    direction_set = set()
                    for j in journeys:
                        transit_legs = [leg for leg in j.get("legs", []) if not is_walk_leg(leg)]
                        if transit_legs:
                            leg = transit_legs[0]
                            line_desig = leg.get("transportation", {}).get("disassembledName")
                            if line_desig:
                                lines_set.add(str(line_desig))
                            direction = leg.get("transportation", {}).get("destination", {}).get("name")
                            if direction:
                                direction_set.add(str(direction))

                    if lines_set:
                        legs[0]["lines"] = sorted(list(lines_set), key=lambda x: int(x) if x.isdigit() else x)
                    if direction_set:
                        legs[0]["direction"] = sorted(list(direction_set))
        else:
            # Query Trips
            o_location_id = origin_stop.get("id")
            d_location_id = dest_stop.get("id")
            url = f"{JOURNEY_API_URL}/trips"
            params = {
                "type_origin": "any",
                "name_origin": o_location_id,
                "type_destination": "any",
                "name_destination": d_location_id,
                "calc_number_of_trips": 3
            }
            if getattr(args, "time", None):
                params["itd_time"] = args.time.replace(":", "")
            if getattr(args, "date", None):
                params["itd_date"] = args.date.replace("-", "")
            res = make_request(url, params)
            if not res or not res.get("journeys"):
                sys.stderr.write("Could not retrieve travel proposals from SL Journey Planner.\n")
                sys.exit(1)
            journeys = res.get("journeys", [])
            if proposal_index < 1 or proposal_index > len(journeys):
                sys.stderr.write(f"Proposal index {proposal_index} out of range (available: 1-{len(journeys)}).\n")
                sys.exit(1)
            
            chosen_journey = journeys[proposal_index - 1]
            legs = []
            for leg in chosen_journey.get("legs", []):
                if is_walk_leg(leg):
                    # Filter out walk legs
                    continue
                line_desig = leg.get("transportation", {}).get("disassembledName")
                o_id_str = extract_site_id(leg.get("origin"))
                o_stop_id = int(o_id_str) if (o_id_str and o_id_str.isdigit()) else 0
                o_name = extract_stop_name(leg.get("origin"))
                d_id_str = extract_site_id(leg.get("destination"))
                d_stop_id = int(d_id_str) if (d_id_str and d_id_str.isdigit()) else 0
                d_name = extract_stop_name(leg.get("destination"))
                
                # Resolve parent site IDs for departures check compatibility
                o_parent_id = get_resolved_parent_id(leg.get("origin"))
                if not o_parent_id:
                    o_parent_id = o_stop_id

                d_parent_id = get_resolved_parent_id(leg.get("destination"))
                if not d_parent_id:
                    d_parent_id = d_stop_id
                
                # Scan all other journeys/legs for alternative transit lines covering this exact same stretch
                lines_set = set()
                if line_desig:
                    lines_set.add(str(line_desig))
                
                for other_j in journeys:
                    for other_leg in other_j.get("legs", []):
                        if is_walk_leg(other_leg):
                            continue
                        other_o_parent_id = get_resolved_parent_id(other_leg.get("origin"))
                        other_d_parent_id = get_resolved_parent_id(other_leg.get("destination"))
                        
                        if other_o_parent_id == o_parent_id and other_d_parent_id == d_parent_id:
                            other_line = other_leg.get("transportation", {}).get("disassembledName")
                            if other_line:
                                lines_set.add(str(other_line))
                
                lines_list = sorted(list(lines_set), key=lambda x: int(x) if x.isdigit() else x)

                # Calculate travel time in minutes
                dep_time = parse_time(leg.get("origin", {}).get("departureTimeEstimated") or leg.get("origin", {}).get("departureTimePlanned"))
                arr_time = parse_time(leg.get("destination", {}).get("arrivalTimeEstimated") or leg.get("destination", {}).get("arrivalTimePlanned"))
                if dep_time and arr_time:
                    dur = int((arr_time - dep_time).total_seconds() / 60)
                else:
                    dur = 0
                
                legs.append({
                    "lines": lines_list,
                    "from": {"id": o_parent_id, "name": o_name, "stop_id": o_stop_id},
                    "to": {"id": d_parent_id, "name": d_name, "stop_id": d_stop_id},
                    "travel_time_minutes": dur
                })
            if not legs:
                sys.stderr.write("No transit legs found in selected travel proposal.\n")
                sys.exit(1)
    else:
        sys.stderr.write("Error: save subcommand expects either 2, 3, or 4 positional arguments.\n")
        sys.exit(1)

    # Remove existing route by name
    routes = [r for r in routes if r.get("name") != name]
    routes.append({
        "name": name,
        "legs": legs
    })
    prefs["favourite_routes"] = routes
    save_prefs(prefs, args.preferences)
    sys.stdout.write(f"Successfully added favorite route: {name}\n")


def cmd_route_remove(args):
    """Remove favorite route."""
    prefs = load_prefs(args.preferences)
    routes = prefs.get("favourite_routes", [])

    filtered = [r for r in routes if r.get("name") != args.name]
    if len(routes) == len(filtered):
        sys.stdout.write(f"Route '{args.name}' not found in favorites.\n")
        return

    prefs["favourite_routes"] = filtered
    save_prefs(prefs, args.preferences)
    sys.stdout.write(f"Successfully removed favorite route: {args.name}\n")


# =====================================================================
# Autonomous Monitoring Engine
# =====================================================================

def parse_time(time_str):
    """Parse API ISO datetime string."""
    if not time_str:
        return None
    try:
        # Strip timezone offset if present for simplicity
        clean_str = time_str.split("+")[0].rstrip("Z")
        return datetime.strptime(clean_str, "%Y-%m-%dT%H:%M:%S")
    except Exception:
        return None


def check_single_site(site_id, site_name, transport_modes, lines, verbose=False):
    """Check departures and deviations for a single site and return issues."""
    warnings = []

    # 1. Check Deviations
    dev_url = f"{DEVIATIONS_API_URL}/messages"
    devs = make_request(dev_url, {"future": False, "site": site_id})
    if devs:
        for dev in devs:
            variants = dev.get("message_variants", [])
            if variants:
                warnings.append({
                    "type": "SITE_DISRUPTION",
                    "message": f"Disruption at {site_name}: {variants[0]['header']}",
                    "details": variants[0].get("details", "")
                })

    # 2. Check Canceled/Delayed Departures
    dep_url = f"{TRANSPORT_API_URL}/sites/{site_id}/departures"
    dep_data = make_request(dep_url, {
        "transport": transport_modes
    })
    if dep_data and lines:
        line_strs = [str(l) for l in lines]
        dep_data["departures"] = [
            d for d in dep_data.get("departures", [])
            if d.get("line", {}).get("designation") in line_strs
        ]
    if dep_data:
        for dep in dep_data.get("departures", []):
            state = dep.get("state", "")
            line = dep.get("line", {}).get("designation", "")
            dest = dep.get("destination", "")
            if state == "CANCELLED":
                warnings.append({
                    "type": "CANCELLED_DEPARTURE",
                    "message": f"Canceled: Line {line} to {dest} at {site_name}"
                })
    return warnings


def cmd_site_check(args):
    """Check departures and active disruptions for one or all favorite sites."""
    prefs = load_prefs(args.preferences)
    stops = prefs.get("favourite_stops", [])

    warnings = []

    if args.site_id:
        site_id = int(args.site_id)
        site_name = f"Site {site_id}"
        transport_modes = None
        lines = None

        # Try to resolve details from favorites
        for s in stops:
            if s.get("id") == site_id:
                site_name = s.get("name", site_name)
                transport_modes = s.get("transport_modes")
                lines = s.get("lines")
                break

        sys.stdout.write(f"Checking site {site_name}...\n")
        warnings.extend(check_single_site(site_id, site_name, transport_modes, lines, args.verbose))
    else:
        if not stops:
            sys.stdout.write("No favorite sites configured to check.\n")
            return

        sys.stdout.write("Checking all favorite sites...\n")
        for s in stops:
            site_id = s["id"]
            site_name = s["name"]
            transport_modes = s.get("transport_modes")
            lines = s.get("lines")
            warnings.extend(check_single_site(site_id, site_name, transport_modes, lines, args.verbose))

    # Output Warnings
    if not warnings:
        sys.stdout.write("Status: OK. No disruptions or cancelled departures detected.\n")
        return

    sys.stdout.write(f"Status: WARNING. Detected {len(warnings)} issues:\n")
    for w in warnings:
        sys.stdout.write(f"- [{w['type']}] {w['message']}\n")
        if args.verbose and w.get("details"):
            sys.stdout.write(f"  Details: {w['details']}\n")


def check_single_route(route, warnings, verbose=False):
    """Check departures and deviations for a single route, printing upcoming departures and warnings for each leg."""
    route_name = route["name"]
    legs = route.get("legs", [])
    leg_departures = []
    route_warnings = []

    sys.stdout.write(f"\nChecking route '{route_name}'...\n")

    for i, leg in enumerate(legs):
        from_site = leg.get("from", {})
        from_id = from_site.get("id")
        from_name = from_site.get("name")
        lines = leg.get("lines", [])
        direction_pref = leg.get("direction")

        # Fetch departures for boarding stop starting from current time
        dep_url = f"{TRANSPORT_API_URL}/sites/{from_id}/departures"
        dep_data = make_request(dep_url)

        # 1. Filter by lines
        if dep_data and lines:
            line_strs = [str(l) for l in lines]
            dep_data["departures"] = [
                d for d in dep_data.get("departures", [])
                if d.get("line", {}).get("designation") in line_strs
            ]

        valid_deps = []
        if dep_data:
            for dep in dep_data.get("departures", []):
                if dep.get("state") == "CANCELLED":
                    continue

                # 2. Filter by direction (case-insensitive destination substring or numeric direction code)
                if direction_pref:
                    if isinstance(direction_pref, list):
                        check_dirs = direction_pref
                    else:
                        check_dirs = [direction_pref]

                    dir_matched = False
                    for p_dir in check_dirs:
                        if str(p_dir) in ["1", "2"]:
                            if dep.get("direction_code") == int(p_dir):
                                dir_matched = True
                                break
                        else:
                            d_dir = dep.get("direction", "")
                            d_dest = dep.get("destination", "")
                            if (p_dir.lower() in d_dir.lower()) or (p_dir.lower() in d_dest.lower()):
                                dir_matched = True
                                break
                    if not dir_matched:
                        continue

                valid_deps.append(dep)

        # 3. Apply Sequential Arrival Filtering for subsequent legs
        if i > 0 and leg_departures[i-1]:
            prev_leg = legs[i-1]
            prev_travel = prev_leg.get("travel_time_minutes") or 0
            first_prev_dep = leg_departures[i-1][0]
            first_prev_time = parse_time(first_prev_dep.get("expected") or first_prev_dep.get("scheduled"))
            if first_prev_time:
                earliest_arrival = first_prev_time + timedelta(minutes=prev_travel)
                # Filter departures to only keep those leaving at or after earliest arrival
                filtered_deps = []
                for dep in valid_deps:
                    dep_time = parse_time(dep.get("expected") or dep.get("scheduled"))
                    if dep_time and dep_time >= earliest_arrival:
                        filtered_deps.append(dep)
                valid_deps = filtered_deps

        leg_departures.append(valid_deps)

        line_csv = ", ".join(str(l) for l in lines)
        line_desc = f"Line {line_csv}" if lines else "Any Line"
        dir_pref = leg.get("direction")
        dir_suffix = ""
        if dir_pref:
            if isinstance(dir_pref, list):
                dir_suffix = f" (toward {', '.join(str(d) for d in dir_pref)})"
            else:
                dir_suffix = f" (toward {dir_pref})"
        to_name = leg.get("to", {}).get("name", "Destination")
        sys.stdout.write(f"Leg {i+1}: {line_desc}{dir_suffix} from {from_name} to {to_name}\n")
        if not valid_deps:
            sys.stdout.write("  - No upcoming departures found\n")
        else:
            now_time = get_stockholm_now()
            for dep in valid_deps[:3]:
                dest = dep.get("destination", "")
                sched = dep.get("scheduled", "")
                expected = dep.get("expected", sched)
                expected_parsed = parse_time(expected)
                expected_str = expected_parsed.strftime("%H:%M") if expected_parsed else expected
                
                # Format with display string, converting absolute clock time to relative minutes and "Nu" to "now"
                display_time = dep.get("display")
                if display_time:
                    if "nu" in display_time.lower():
                        display_str = "now"
                    elif "min" in display_time.lower():
                        display_str = display_time.lower()
                    else:
                        if expected_parsed:
                            diff_mins = int((expected_parsed - now_time).total_seconds() / 60)
                            display_str = f"{diff_mins} min" if diff_mins > 0 else "now"
                        else:
                            display_str = display_time
                else:
                    if expected_parsed:
                        diff_mins = int((expected_parsed - now_time).total_seconds() / 60)
                        display_str = f"{diff_mins} min" if diff_mins > 0 else "now"
                    else:
                        display_str = ""

                # Format time string with estimated arrival if travel time is configured
                travel_time = leg.get("travel_time_minutes") or 0
                time_range_str = expected_str
                if travel_time > 0 and expected_parsed:
                    arr_parsed = expected_parsed + timedelta(minutes=travel_time)
                    arr_str = arr_parsed.strftime("%H:%M")
                    time_range_str = f"{expected_str} -> ~{arr_str}"

                line_no = dep.get("line", {}).get("designation", "")
                line_prefix = f"Line {line_no} to {dest}: " if line_no else ""

                if display_str:
                    sys.stdout.write(f"  - {line_prefix}{time_range_str} -- {display_str}\n")
                else:
                    sys.stdout.write(f"  - {line_prefix}{time_range_str}\n")

        # Fetch deviations affecting this leg (site or line)
        dev_url = f"{DEVIATIONS_API_URL}/messages"
        seen_dev_headers = set()

        # 1. Query station-wide deviations for this boarding site
        site_devs = make_request(dev_url, {"future": False, "site": from_id})
        if site_devs:
            for dev in site_devs:
                variants = dev.get("message_variants", [])
                if variants:
                    header = variants[0]['header']
                    if header not in seen_dev_headers:
                        seen_dev_headers.add(header)
                        route_warnings.append({
                            "type": "STATION_DISRUPTION",
                            "leg": i + 1,
                            "message": header,
                            "details": variants[0].get("details", "")
                        })

        # 2. Query line-specific deviations for this leg
        for line_id in lines:
            line_devs = make_request(dev_url, {"future": False, "line": line_id})
            if line_devs:
                for dev in line_devs:
                    # Apply strict deviation assessment
                    stop_areas = dev.get("scope", {}).get("stop_areas", [])
                    affected_stop_ids = [sa.get("id") for sa in stop_areas if sa.get("id")]
                    if affected_stop_ids and from_id not in affected_stop_ids:
                        continue

                    variants = dev.get("message_variants", [])
                    if variants:
                        header = variants[0]['header']
                        if header not in seen_dev_headers:
                            seen_dev_headers.add(header)
                            route_warnings.append({
                                "type": "ROUTE_DISRUPTION",
                                "leg": i + 1,
                                "message": header,
                                "details": variants[0].get("details", "")
                            })

    # Evaluate Connections between sequential legs
    for i in range(len(legs) - 1):
        leg1 = legs[i]
        leg2 = legs[i+1]
        travel_time = leg1.get("travel_time_minutes")

        if not travel_time:
            continue

        deps1 = leg_departures[i]
        deps2 = leg_departures[i+1]

        for d1 in deps1[:3]:
            d1_time = parse_time(d1.get("expected") or d1.get("scheduled"))
            if not d1_time:
                continue

            arrival_time = d1_time + timedelta(minutes=travel_time)

            # Find the first departure on leg 2 after arrival
            matching_d2 = None
            for d2 in deps2:
                d2_time = parse_time(d2.get("expected") or d2.get("scheduled"))
                if d2_time and d2_time >= arrival_time:
                    matching_d2 = d2
                    break

            if matching_d2:
                d2_time = parse_time(matching_d2.get("expected") or matching_d2.get("scheduled"))
                buffer = (d2_time - arrival_time).total_seconds() / 60
                if buffer < 5.0:
                    line1 = d1.get("line", {}).get("designation", "")
                    line2 = matching_d2.get("line", {}).get("designation", "")
                    from_name_val = leg1.get("from", {}).get("name", "Origin")
                    d2_dir = matching_d2.get("direction", "destination")
                    route_warnings.append({
                        "type": "TIGHT_CONNECTION",
                        "leg": i + 1,
                        "message": f"({line1} leaving {from_name_val} at {d1_time.strftime('%H:%M')}, expected arrival {arrival_time.strftime('%H:%M')}) to Leg {i+2} ({line2} toward {d2_dir} departing at {d2_time.strftime('%H:%M')}) has only {int(buffer)} min buffer (min required: 5 min)."
                    })

    # Output route-specific warnings immediately below departures
    if route_warnings:
        sys.stdout.write("Warnings:\n")
        grouped = {}
        order = []
        for rw in route_warnings:
            key = (rw["type"], rw["leg"])
            if key not in grouped:
                grouped[key] = []
                order.append(key)
            grouped[key].append(rw)

        for (w_type, leg_num) in order:
            items = grouped[(w_type, leg_num)]
            leg_label = f"Leg {leg_num}"

            if w_type == "STATION_DISRUPTION":
                header_label = f"Station disruption on {leg_label}"
            elif w_type == "ROUTE_DISRUPTION":
                header_label = f"Route disruption on {leg_label}"
            elif w_type == "TIGHT_CONNECTION":
                header_label = f"Tight connection on {leg_label}"
            else:
                header_label = f"{w_type} on {leg_label}"

            if len(items) == 1:
                sys.stdout.write(f"  - {header_label}: {items[0]['message']}\n")
                if verbose and items[0].get("details"):
                    sys.stdout.write(f"    Details: {items[0]['details']}\n")
            else:
                sys.stdout.write(f"  - {header_label}:\n")
                for item in items:
                    sys.stdout.write(f"    - {item['message']}\n")
                    if verbose and item.get("details"):
                        sys.stdout.write(f"      Details: {item['details']}\n")

    warnings.extend(route_warnings)


def cmd_route_check(args):
    """Check departures and connection safety buffer for one or all favorite routes."""
    prefs = load_prefs(args.preferences)
    routes = prefs.get("favourite_routes", [])

    warnings = []

    if args.alias:
        target = None
        for r in routes:
            if r.get("name") == args.alias:
                target = r
                break
        if not target:
            sys.stderr.write(f"Route '{args.alias}' not found in favorites.\n")
            sys.exit(1)

        check_single_route(target, warnings, verbose=args.verbose)
    else:
        if not routes:
            sys.stdout.write("No favorite routes configured to check.\n")
            return

        sys.stdout.write("Checking all favorite routes...\n")
        for r in routes:
            check_single_route(r, warnings, verbose=args.verbose)




# =====================================================================
# Main Parser
# =====================================================================

def _validate_direction(value):
    """Validate --direction argument: accept numeric codes 1 or 2, reject destination names with a clear error."""
    try:
        v = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"'{value}' is not a valid direction. --direction accepts numeric codes only (1 or 2), "
            f"not destination names like 'Märsta' or 'Uppsala C'."
        )
    if v not in (1, 2):
        raise argparse.ArgumentTypeError(f"{v} is not a valid direction code. Use 1 or 2.")
    return v


def main():
    parser = argparse.ArgumentParser(description="SL Trafiklab CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # site namespace
    p_site = subparsers.add_parser("site", help="Site operations")
    site_sub = p_site.add_subparsers(dest="subcommand", help="Site subcommands")

    # site list
    p_list = site_sub.add_parser("list", help="Search/List sites")
    p_list.add_argument("query", help="Search string for stop names")
    p_list.add_argument("--limit", type=int, default=10, help="Maximum search results")

    # site departures
    p_dep = site_sub.add_parser("departures", help="Fetch departures for a site")
    p_dep.add_argument("site_id", help="Numeric Site ID")
    p_dep.add_argument("--line", help="Filter by line designation")
    p_dep.add_argument("--transport", help="Filter by transport mode (BUS, METRO, TRAIN, etc.)")
    p_dep.add_argument("--direction", type=lambda v: _validate_direction(v), help="Filter by direction code (1 or 2). Numeric codes only — do NOT pass destination names like 'Märsta'.")
    p_dep.add_argument("--forecast", type=int, help="Forecast window in minutes")

    # site check
    p_site_chk = site_sub.add_parser("check", help="Check departures and disruptions for one or all favorite sites")
    p_site_chk.add_argument("site_id", nargs="?", help="Optional numeric Site ID to check a single station")
    p_site_chk.add_argument("--preferences", help="Override preferences file path")
    p_site_chk.add_argument("-v", "--verbose", action="store_true", help="Print details of deviations")

    # site save
    p_site_save = site_sub.add_parser("save", help="Save favorite site")
    p_site_save.add_argument("site_id", help="Numeric Site ID")
    p_site_save.add_argument("name", help="Display name for favorite site")
    p_site_save.add_argument("--lines", help="Comma-separated line filters")
    p_site_save.add_argument("--modes", help="Comma-separated transport mode filters")
    p_site_save.add_argument("--preferences", help="Override preferences file path")

    # site remove
    p_site_rem = site_sub.add_parser("remove", help="Remove favorite site")
    p_site_rem.add_argument("site_id", help="Site ID to remove")
    p_site_rem.add_argument("--preferences", help="Override preferences file path")

    # deviations namespace
    p_dev = subparsers.add_parser("deviations", help="Fetch transit deviations")
    p_dev.add_argument("--site", help="Filter by Site ID")
    p_dev.add_argument("--line", help="Filter by line designation")
    p_dev.add_argument("--future", type=bool, default=False, help="Show planned/future deviations")
    p_dev.add_argument("-v", "--verbose", action="store_true", help="Print deviation details")

    # route namespace
    p_route = subparsers.add_parser("route", help="Route operations")
    route_sub = p_route.add_subparsers(dest="subcommand", help="Route subcommands")

    # route check
    p_route_chk = route_sub.add_parser("check", help="Check departures and connection safety buffers for one or all routes")
    p_route_chk.add_argument("alias", nargs="?", help="Optional Route alias to check a single route")
    p_route_chk.add_argument("--preferences", help="Override preferences file path")
    p_route_chk.add_argument("-v", "--verbose", action="store_true", help="Print details of disruptions")

    # route save
    p_route_save = route_sub.add_parser("save", help="Save favorite route")
    p_route_save.add_argument("args", nargs="+", help="Arguments: either <alias> <legs_json> OR <origin> <destination> [<proposal_index>] <alias>")
    p_route_save.add_argument("--preferences", help="Override preferences file path")
    p_route_save.add_argument("--time", help="Optional travel time in HH:MM format for querying dynamic proposals")
    p_route_save.add_argument("--date", help="Optional travel date in YYYY-MM-DD format for querying dynamic proposals")

    # route find
    p_route_find = route_sub.add_parser("find", help="Find travel proposals dynamically using SL Journey Planner")
    p_route_find.add_argument("origin_or_alias", help="Origin stop name, Site ID, or saved route alias")
    p_route_find.add_argument("destination", nargs="?", help="Destination stop name or Site ID (optional if alias is used)")
    p_route_find.add_argument("--preferences", help="Override preferences file path")
    p_route_find.add_argument("--all", action="store_true", help="Bypass leg preference filtering and display all options")
    p_route_find.add_argument("--time", help="Optional travel time in HH:MM format")
    p_route_find.add_argument("--date", help="Optional travel date in YYYY-MM-DD format")
    p_route_find.add_argument("--number", type=int, default=3, choices=[1, 2, 3], help="Number of travel options to return (1-3)")
    p_route_find.add_argument("--via", help="Optional intermediate stop name (e.g. 'Hornstull') or Site ID (e.g. 9192) to travel through")
    p_route_find.add_argument("--dwell-time", help="Optional dwell time at the via stop in HH:MM or HHMM format (e.g. 00:15 or 0015)")
    p_route_find.add_argument("--not-via", help="Optional stop name (e.g. 'Slussen') or Site ID (e.g. 9102) to avoid")

    # route remove
    p_route_rem = route_sub.add_parser("remove", help="Remove favorite route")
    p_route_rem.add_argument("name", help="Route alias to remove")
    p_route_rem.add_argument("--preferences", help="Override preferences file path")

    args = parser.parse_args()

    # Routing
    if args.command == "site":
        if args.subcommand == "list":
            cmd_site_list(args)
        elif args.subcommand == "departures":
            cmd_site_departures(args)
        elif args.subcommand == "check":
            cmd_site_check(args)
        elif args.subcommand == "save":
            cmd_site_save(args)
        elif args.subcommand == "remove":
            cmd_site_remove(args)
        else:
            p_site.print_help()
    elif args.command == "route":
        if args.subcommand == "check":
            cmd_route_check(args)
        elif args.subcommand == "save":
            cmd_route_save(args)
        elif args.subcommand == "find":
            cmd_route_find(args)
        elif args.subcommand == "remove":
            cmd_route_remove(args)
        else:
            p_route.print_help()
    elif args.command == "deviations":
        cmd_deviations(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

