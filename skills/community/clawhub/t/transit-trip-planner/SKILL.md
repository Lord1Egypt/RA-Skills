---
name: "transit-trip-planner"
description: "AirnodeHub transit skill to plan transit, walking, and driving trips; compare routes, check live departures or disruptions, geocode places, and verify Airnode attestations."
---

# Transit Trip Planner

## Execute

1. Extract origin, destination, departure or arrival time, mode, accessibility needs, and route constraints. Geocode ambiguous places and confirm only when different matches materially alter the trip. **Done when:** endpoints and time are routable.

2. Read current documentation at `https://airnode-busmaps.fly.dev/` and `https://airnode-geoapify.fly.dev/`. Use only documented POST operations and coordinate order; GET only reads documentation. **Done when:** operation schemas, costs, and attribution requirements are known.

3. Choose the narrowest operation: BusMaps `planJourney` for transit, `walkRoute` for walking, `driveRoute` for driving, `alerts` for a known route, and `stopsInRadius` plus `nextDepartures` for nearby live departures. Use Geoapify `routing` when BusMaps lacks coverage or specialist requirements such as cycling, trucks, avoid rules, or ordered waypoints apply. Use matrix operations only for multiple origins or destinations. **Done when:** the minimum route plan is selected.

4. Prefer adequate free operations. Before Geoapify or any potentially paid POST, state the bounded scope and known or uncertain cost and obtain explicit approval. Never silently expand a paid query. **Done when:** cost is free, approved, or blocked before calling.

5. POST `{"operation":"<operation>","parameters":{...}}` to the selected listing. Preserve explicit timezone offsets; otherwise treat BusMaps times as local to the origin. Read notices and distinguish `noCoverage` from `noRouteFound`. Do not claim real-time status when live fields are absent. **Done when:** an attested route response or exact error is received.

6. Present the recommended route, departure/arrival, duration, distance, transfers, walking legs, disruptions, accessibility caveats, freshness, cost, and verification status. Label approximated transit or fallback estimates. Whenever Geoapify contributes, include `Powered by Geoapify` and preserve its datasource attribution. **Done when:** the route is actionable and provenance is visible.

## Verification

Require `airnode`, `requestHash`, `timestamp`, `data`, and `signature`; check endpoint plausibility and freshness. Cryptographically verify the documented request hash and EIP-191 signer when tooling is available; otherwise state that the attestation was not cryptographically verified. Confirm paid calls were approved and attribution was preserved.
