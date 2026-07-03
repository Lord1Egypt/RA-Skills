# SL Deviations API Reference

This document describes the endpoints and query parameters for the SL Deviations API.

**Base URL**: `https://deviations.integration.sl.se/v1`

---

## Endpoints

### 1. `GET /messages`
Returns a list of active or future deviation messages (the latest version of publishable deviation messages).

#### Query Parameters
*   **`future`** (boolean, optional): Include future deviations (planned maintenance, etc.).
*   **`transport_authority`** (integer, optional): Filter on a specific transport authority ID.
*   **`site`** (array of strings, optional): Filter results to only include these site IDs.
*   **`line`** (array of strings, optional): Filter results to only include these line numbers.
*   **`transport_mode`** (array of strings, optional): Filter results to only include this transport mode.

#### Headers
*   **`Accept-Encoding`** (string, optional): Set to `gzip` to enable compressed responses if supported by the client.
