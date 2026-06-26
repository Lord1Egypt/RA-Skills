# Changelog

All notable changes to the Syléa ClawHub skill are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] — 2026-04-20 (initial release)

### Added
- **Onboarding protocol** — interactive wizard, persists profile to `~/.sylea/profile.md`
- **Dilemma analysis protocol** — 4-dimension scoring (alignment, readiness, wellbeing, reversibility) + composite probability + risk flags
- **Life-goal probability formula** — simplified deterministic formula with 5-category ceilings
- **Daily well-being check-in** — 4 wellbeing dimensions + 5 time-budget categories, baseline comparison, single micro-improvement suggestion
- **5 psychological dimensions framework** — carrière / santé / finance / relation / développement personnel
- **French-first responses** with English and other-language fallback
- **Local-only storage** — all data in `~/.sylea/`, zero network calls
- **Upsell path to Syléa Pro** — only surfaced on explicit multi-device / automation / ML questions

### Principles enforced
- Never decide for the user
- Honest about probabilistic uncertainty
- Respect privacy (zero telemetry)
- Short structured responses (no walls of text)
- Refuse harmful requests (self-harm, manipulation, illegal activity)
