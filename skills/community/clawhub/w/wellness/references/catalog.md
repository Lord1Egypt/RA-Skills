# Wellness source catalog (Tier 1 + Tier 2)

This catalog is user-facing: it lists common wellness apps/devices and how to connect them.

Legend:
- Tier 1: official personal authorization (OAuth/API key) that individual users can complete
- Tier 2: phone OS aggregator (Apple Health / Android Health Connect) via a local bridge

## Tier 1 — Apps / services (official personal auth)

### Wearables / sleep / recovery

- WHOOP (sleep, recovery, strain)
  - Connect: OAuth (official)
  - Skill: `openclaw-whoop`

- Oura Ring (sleep, readiness, activity)
  - Connect: Personal Access Token (Tier 1)
  - Skill: `openclaw-oura`

- Fitbit (sleep, activity, heart)
  - Connect: OAuth
  - Skill: `openclaw-fitbit`

- Withings (weight, body fat, BP, and sleep summary where available)
  - Connect: OAuth
  - Skill: `openclaw-withings`

### Workouts / training logs

- Strava (runs/rides/workouts)
  - Connect: OAuth
  - Skill: TBD (`openclaw-strava`)

### Sleep environment

- Eight Sleep (bed temp + sleep/session)
  - Connect: account token via `eightctl`
  - Skill: existing OpenClaw skill: `eightctl` (can be orchestrated by the hub)

### Nutrition / hydration (availability varies)

- Cronometer (nutrition)
  - Connect: API (varies by plan) / export
  - Skill: TBD

- MyFitnessPal (nutrition)
  - Connect: API availability varies; may require partner access
  - Skill: TBD

## Tier 2 — OS health aggregators (requires phone-side bridge)

- Apple Health (iOS / HealthKit)
  - Connect: user grants HealthKit permissions on-device
  - Hub needs: a phone-side bridge to export/sync daily aggregates to OpenClaw

- Android Health Connect
  - Connect: user grants permissions on-device
  - Hub needs: a phone-side bridge to export/sync daily aggregates to OpenClaw

## Next: expand list

Add more sources as independent skills. Keep the hub stable.
