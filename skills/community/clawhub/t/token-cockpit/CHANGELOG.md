# Changelog

All notable changes to Token Cockpit are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/); this project adheres to semantic versioning.

## [1.0.0] - 2026-05-23

Initial release.

### Added
- `report` command: spend and token breakdown by model with a monthly projection from the observed daily rate.
- `budget` command: compares spend or projected monthly spend against a limit and emits a tiered alert (OK / WARN at 80% / OVER at 100%).
- `route` command: finds small calls (default <2,000 tokens) running on premium models and estimates savings from downgrading to a cheaper tier.
- `simulate` command: what-if savings of moving one model's traffic to another.
- Tolerant log loader: accepts JSONL or JSON array, multiple token field-name variants, nested `usage` objects, and epoch or ISO timestamps.
- Editable default price table with `--pricing` JSON override; unknown models are counted as $0 and flagged so totals are never silently wrong.
- Auto-detection of common OpenClaw usage-log locations with `--logs` override.
- Bundled `sample_usage.jsonl` for immediate demonstration.
- Zero required dependencies: pure Python standard library.
