# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] — 2026-05-13

### Changed
- Frontmatter `version` field now quoted as a string per ClawHub CLI requirements
- Added this CHANGELOG.md for consistency with the rest of the published skill catalog

### Notes
- No behavior changes in this release. Purely documentation and metadata cleanup.

## [1.0.0] — 2026-04-12

### Added
- Initial release
- Multi-vehicle service history tracking (cars, trucks, SUVs, motorcycles, boats, RVs, trailers)
- Service records with date, mileage, work performed, mechanic, and cost
- Built-in maintenance knowledge with mileage and time-based intervals
- Mechanic directory with notes and pricing history
- Registration and insurance renewal tracking with reminders
- Cost tracking with per-vehicle and per-year rollups
- Proactive maintenance prompts based on mileage and elapsed time
- Persistent storage in `vehicle-data.json`
