# SL Journey Planner v2 - Trips API Reference

This document describes the query parameters for the SL Journey Planner v2 `trips` endpoint.

**Base URL**: `https://journeyplanner.integration.sl.se/v2/trips`

---

## Query Parameters

### 1. Route Terminals (Required)
*   **`type_origin`**: Origin input type (`any` for stop names/addresses, `coord` for WGS84 coordinates).
*   **`name_origin`**: Stop ID or coordinates. Coordinate format: `"<x>:<y>:WGS84[dd.ddddd]"`.
*   **`type_destination`**: Destination input type (`any` or `coord`).
*   **`name_destination`**: Stop ID or coordinates.

### 2. Search Window & Results
*   **`calc_number_of_trips`**: Number of travel proposals to return (Integer: `1` to `3`).
*   **`calc_one_direction`**: If `true`, prevents the planner from calculating one trip departing before the requested departure time (default is `false`).

### 3. Date and Time (Temporal Parameters)
*   **`itd_date`**: The date of the trip in **`YYYYMMDD`** format (e.g., `20260703`).
*   **`itd_time`**: The time of the trip in **`HHMM`** format (e.g., `0700`).
*   **`itd_trip_date_time_dep_arr`**: Search for departure time or arrival time. Expected values: `"dep"` (departure) or `"arr"` (arrival). Defaults to `"dep"`.

### 4. Routing Options (Optional)
*   **`route_type`**: Route prioritization model. Expected values:
    *   `leasttime` (fastest connection, default)
    *   `leastinterchange` (fewest transfers)
    *   `leastwalking` (shortest walking leg distance)
*   **`max_changes`**: Maximum transfers permitted (Integer: `0` to `9`).
*   **`language`**: Response language (`sv` or `en`).
*   **`gen_c`**: Include leg coordinate sequences (`true` or `false`).

### 5. Via Stops (Optional)
*   **`type_via`** / **`name_via`**: Intermediate stop to travel through.
*   **`dwell_time`**: Time to wait at the via stop in `HHMM` format.
*   **`type_not_via`** / **`name_not_via`**: Stop ID to avoid.

### 6. Transport Mode Filters (Optional)
Specify `true` (default) or `false` to include/exclude specific transport modes:
*   **`incl_mot_0`**: Commuter train (*pendeltåg*)
*   **`incl_mot_2`**: Metro (*tunnelbana*)
*   **`incl_mot_4`**: Local train/tram (*lokaltåg/spårväg*)
*   **`incl_mot_5`**: Bus (*buss*)
*   **`incl_mot_9`**: Ship and ferry (*båttrafik*)
*   **`incl_mot_10`**: On-demand traffic
*   **`incl_mot_14`**: National train (*fjärrtåg*)
*   **`incl_mot_19`**: Accessible bus (*närtrafik*)
