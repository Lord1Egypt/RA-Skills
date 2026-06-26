# RollingGo MCP Reference

> Load this file for RollingGo Flight MCP execution environment.
> Flight search logic and filter rules → `SKILL.md`.

## Table of Contents

1. [MCP Server](#mcp-server)
2. [API Key Setup](#api-key-setup)
3. [Tool Guide](#tool-guide)
4. [End-to-End Workflows](#end-to-end-workflows)
5. [Troubleshooting](#troubleshooting)
6. [Client Configuration](#client-configuration)

---

## MCP Server

Server name: `RollingGo-Flight-MCP`

```json
{
  "mcpServers": {
    "RollingGo-Flight-MCP": {
      "url": "https://mcp.rollinggo.cn/mcp/flight",
      "type": "streamable_http"
    }
  }
}
```

Transport: `streamable_http`

Current public online configuration does not require a client-side Bearer Token.

---

## API Key Setup

No key is required for the current public online MCP configuration.

If a private deployment or business channel requires authentication, configure headers according to the actual environment:

```json
{
  "mcpServers": {
    "RollingGo-Flight-MCP": {
      "url": "https://mcp.rollinggo.cn/mcp/flight",
      "type": "streamable_http",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

Apply at: https://rollinggo.store/apply

---

## Tool Guide

### `searchAirports`

Required: `keyword`

Purpose: search airports, cities, airport codes, or related traffic nodes.

```json
{ "keyword": "杭州" }
```

```json
{ "keyword": "HGH" }
```

Returned fields commonly include:

```json
{
  "message": "机场搜索成功",
  "airPortInformationList": [
    {
      "airportCode": "TFU",
      "airportName": "Tianfu Airport",
      "cityCode": "CTU",
      "cityName": "Chengdu",
      "countryCode": "CN",
      "countryName": "China",
      "timeZone": "+08:00"
    }
  ]
}
```

Use `airportCode` as `fromAirport` / `toAirport` when the user specifies a concrete airport. Use `cityCode` as `fromCity` / `toCity` for broader city-level searches.

### `searchFlights`

Required parameters:

- `adultNumber`: integer
- `childNumber`: integer, use `0` when no children
- `cabinGrade`: `ECONOMY` | `PREMIUM_ECONOMY` | `BUSINESS` | `FIRST`
- `tripType`: `ONE_WAY` | `ROUND_TRIP`
- `fromDate`: `YYYY-MM-DD`
- `retDate`: required for `ROUND_TRIP`
- Origin: one of `fromCity` or `fromAirport`
- Destination: one of `toCity` or `toAirport`

Minimal one-way example:

```json
{
  "adultNumber": 1,
  "childNumber": 0,
  "cabinGrade": "ECONOMY",
  "fromCity": "HGH",
  "toCity": "CTU",
  "fromDate": "2026-05-01",
  "tripType": "ONE_WAY"
}
```

Round-trip example:

```json
{
  "adultNumber": 1,
  "childNumber": 0,
  "cabinGrade": "ECONOMY",
  "fromCity": "HGH",
  "toCity": "CTU",
  "fromDate": "2026-05-01",
  "retDate": "2026-05-05",
  "tripType": "ROUND_TRIP"
}
```

Returned fields commonly include:

```json
{
  "message": "航班搜索成功",
  "flightInformationList": [
    {
      "routingId": "...",
      "totalAdultPrice": 1813.0,
      "totalChildPrice": 0.0,
      "currency": "CNY",
      "fromSmartValueScore": 95.0,
      "validatingCarrier": "3U",
      "fromSegments": [
        {
          "flightNumber": "3U8916",
          "depTime": "2026-05-01T17:50:00",
          "arrTime": "2026-05-01T21:00:00",
          "depAirport": "HGH",
          "arrAirport": "CTU",
          "duration": "190",
          "stopCities": ""
        }
      ],
      "retSegments": []
    }
  ]
}
```

Key fields in each `flightInformationList` entry:

| Field | Type | Notes |
|---|---|---|
| `totalAdultPrice` | number | Per-adult total price |
| `totalChildPrice` | number | Per-child total price; `0.0` when no children |
| `currency` | string | e.g. `"CNY"` |
| `fromSmartValueScore` | number | 0–100; higher = better value composite score |
| `validatingCarrier` | string | IATA airline code |
| `fromSegments` | array | Outbound flight legs |
| `retSegments` | array | Return legs; empty array for one-way |

Key fields in each segment:

| Field | Type | Notes |
|---|---|---|
| `flightNumber` | string | e.g. `"3U8916"` |
| `depTime` / `arrTime` | string | ISO 8601 datetime |
| `depAirport` / `arrAirport` | string | IATA airport code |
| `duration` | string | Flight duration in **minutes** (e.g. `"190"` = 3h10m) |
| `stopCities` | string | Empty string = direct flight; otherwise comma-separated stop city codes |

---

## End-to-End Workflows

### Workflow 1: City name → airport/city code → one-way flight search

Step 1: resolve origin (call 1 of 2).

```json
{ "keyword": "杭州" }
```

Step 1: resolve destination (call 2 of 2).

```json
{ "keyword": "成都" }
```

Step 2: use returned `cityCode` values for broad search.

```json
{
  "adultNumber": 1,
  "childNumber": 0,
  "cabinGrade": "ECONOMY",
  "fromCity": "HGH",
  "toCity": "CTU",
  "fromDate": "2026-05-01",
  "tripType": "ONE_WAY"
}
```

### Workflow 2: Specific airport → airport-level search

If user says "上海虹桥到成都天府", resolve both airport names and use airport codes.

Step 1: resolve origin airport (call 1 of 2).

```json
{ "keyword": "虹桥" }
```

Step 1: resolve destination airport (call 2 of 2).

```json
{ "keyword": "天府" }
```

Step 2: call `searchFlights` with `fromAirport` and `toAirport`.

### Workflow 3: Round trip

Use `tripType=ROUND_TRIP` and include `retDate`.

```json
{
  "adultNumber": 2,
  "childNumber": 0,
  "cabinGrade": "ECONOMY",
  "fromCity": "HGH",
  "toCity": "CTU",
  "fromDate": "2026-05-01",
  "retDate": "2026-05-05",
  "tripType": "ROUND_TRIP"
}
```

---

## Troubleshooting

- **No airport returned:** Try Chinese name, English name, city name, or IATA code.
- **Multiple airports returned:** Use city-level code for broad search, airport-level code for exact airport requirements.
- **No flights returned:** Switch from airport code to city code, check date format, check `retDate` for round trips, or ask whether nearby dates are acceptable.
- **Validation issue:** Confirm required parameters: `adultNumber`, `childNumber`, `cabinGrade`, `tripType`, `fromDate`, origin code, destination code.
- **Price looks unstable:** Normal real-time supplier behavior; re-query before final presentation or booking handoff.
- **User asks to book/pay/refund/change:** Explain that the documented MCP tools currently cover flight search, not order operations.

---

## Client Configuration

The core configuration is identical across all MCP clients that support `streamable_http`. See [MCP Server](#mcp-server) for the JSON block.

Different clients may use slightly different wrapper keys (e.g. `mcpServers` vs `servers`), but the `url` and `type` fields are standard.

For clients that require authentication headers, see [API Key Setup](#api-key-setup).
