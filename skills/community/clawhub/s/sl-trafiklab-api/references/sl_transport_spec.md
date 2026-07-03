# SL Transport API Reference

This document describes the endpoints and query parameters for the SL Transport API (which includes lines, sites, stop points, and departures).

**Base URL**: `https://transport.integration.sl.se/v1`

---

## Endpoints

### 1. `GET /lines`
List all lines within Region Stockholm.

#### Query Parameters
*   **`transport_authority_id`** (string, required): Filter by transport authority ID (e.g. `"1"` for SL).

#### Headers
*   **`Accept-Encoding`** (string, optional): Set to `gzip` to request compressed responses.

---

### 2. `GET /sites`
List all sites (parent transit stations) within Region Stockholm.

#### Query Parameters
*   **`expand`** (boolean, optional): Set to `true` to expand referenced objects in the response. Enabling this significantly increases response size and query time.

#### Headers
*   **`Accept-Encoding`** (string, optional): Set to `gzip` to request compressed responses.

---

### 3. `GET /sites/{id}/departures`
Get upcoming departures and deviations starting from the time of the request (returns a maximum of 3 departures for each line and direction).

#### Path Parameters
*   **`id`** (string, required): The numeric parent Site ID (e.g., `"1386"`).

#### Query Parameters
*   **`transport`** (string, optional): Filter by transport mode enum (e.g. `BUS`, `METRO`, `TRAIN`).
*   **`direction`** (string, optional): Filter by direction code (e.g., `1` or `2`).
*   **`line`** (string, optional): Filter by a specific line number.
*   **`forecast`** (integer, optional): Defines the window of time in minutes for which to fetch departures starting from now (e.g., `30` minutes).

---

### 4. `GET /stop-points`
List all individual stop-points (platform-level coordinates and tracks) within Region Stockholm.

#### Headers
*   **`Accept-Encoding`** (string, optional): Set to `gzip` to request compressed responses.

---

### 5. `GET /transport-authorities`
List all transport authorities within Region Stockholm.

#### Headers
*   **`Accept-Encoding`** (string, optional): Set to `gzip` to request compressed responses.
