# rivian-ls JSON Field Reference

All fields returned by `rivian-ls status --format json`:

| Field | Type | Description |
|-------|------|-------------|
| VehicleID | string | Internal vehicle identifier |
| VIN | string | Vehicle Identification Number |
| Name | string | User-set vehicle name |
| Model | string | Rivian model (e.g. "R1T", "R1S") |
| UpdatedAt | ISO 8601 | Timestamp of last data fetch |
| BatteryLevel | float | State of charge (0–100%) |
| BatteryCapacity | float | Usable capacity in kWh |
| RangeEstimate | float | Estimated range in miles |
| ChargeState | string | "charging", "complete", "disconnected" |
| ChargeLimit | int | Target charge limit (%) |
| ChargingRate | float\|null | Current charge rate in kW (null if not charging) |
| TimeToCharge | string\|null | Human-readable time to charge limit |
| Location.Latitude | float | GPS latitude |
| Location.Longitude | float | GPS longitude |
| Location.UpdatedAt | ISO 8601 | Timestamp of last location update |
| CabinTemp | float\|null | Interior temperature in °F |
| ExteriorTemp | float\|null | Outside temperature in °F |
| IsLocked | bool | True if all doors locked |
| IsOnline | bool | True if vehicle is connected |
| Odometer | float | Total miles driven |
| Doors.FrontLeft | string | "closed" or "open" |
| Doors.FrontRight | string | "closed" or "open" |
| Doors.RearLeft | string | "closed" or "open" |
| Doors.RearRight | string | "closed" or "open" |
| Windows.FrontLeft | string | "closed" or "open" |
| Windows.FrontRight | string | "closed" or "open" |
| Windows.RearLeft | string | "closed" or "open" |
| Windows.RearRight | string | "closed" or "open" |
| Frunk | string | "closed", "open", or "unknown" |
| Liftgate | string | "closed", "open", or "unknown" |
| TonneauCover | string | "closed", "open", or "unknown" (R1T bed cover) |
| TirePressures.FrontLeft | float | PSI (0 if unavailable) |
| TirePressures.FrontRight | float | PSI |
| TirePressures.RearLeft | float | PSI |
| TirePressures.RearRight | float | PSI |
| TirePressures.FrontLeftStatus | string | "OK" or warning string |
| TirePressures.FrontRightStatus | string | "OK" or warning string |
| TirePressures.RearLeftStatus | string | "OK" or warning string |
| TirePressures.RearRightStatus | string | "OK" or warning string |
| ReadyScore | float | Rivian's computed vehicle readiness (0–100%) |
| RangeStatus | string | "normal", "low", or "critical" |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Authentication failure |
| 2 | Vehicle not found |
| 3 | API error / network failure |
| 4 | Invalid arguments |

## Known Limitations

- Tire PSI fields return 0 when the vehicle hasn't recently provided pressure data
- Liftgate and TonneauCover may return "unknown" depending on vehicle trim
- WebSocket subscriptions may fail; rivian-ls auto-falls back to polling
- This uses an **unofficial** Rivian API — may break without notice
