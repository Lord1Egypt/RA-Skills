# Changelog

All notable changes to the `S2-DaoKernel` plugin will be documented in this file.


## [1.2.5] - 2026-05-10
### added
update: DAO.md

## [1.2.1] - 2026-05-10
### Added
chore: V1.2.1 - Enhanced privacy prompts in DAO.py and added offline ID disclaimers per ClawHub advisories

## [1.2.0] - 2026-05-10
### Added
- **Offline Incarnation Wizard**: Completely rewrote `DAO.py` to act as an interactive setup wizard.
- **Geo-Hash Addressing**: Implemented an MD5-based hashing algorithm that converts physical addresses into consistent 6-segment Taohuayuan coordinates completely offline.
- **Instant S2-DID Generation**: Added support for local generation of the 22-character S2-DID, supporting 5 agent archetypes (General, Companion, Pet, Embodied, Digital Human).
- **Lazy Validation Pipeline**: Enabled developers to start locally immediately, with the option to verify their agent's ID later at `taohuayuan.world`.

## [1.1.3] - 2026-05-10
### Added
fix: V1.1.3 - Resolved semantic warnings on memory persistence and added User Override protocol

## [1.1.2] - 2026-05-10
### Added
V1.1.2 - Enhanced memory privacy, fixed repo URL, and added security headers

## [1.1.1] - 2026-05-10
### Added
Security Patch: Added explicit consent protocols for IoT devices and fixed case-sensitive path resolution to comply with ClawHub safety guidelines.

## [1.1.0] - 2026-05-09
### Added
- **ClawHub Release**: Initial official packaging for the OpenClaw ecosystem.
- **8 Regional Daos**: Introduced domain-specific physical causality rules (`EATH`, `MARS`, `MOON`, `META`, `FILM`, `GAME`, `ACGN`, `MYTH`).
- **Interactive Injection**: Added `DAO.py` for dynamic `soul.md` snippet generation based on S2-DID addressing.
- **i18n Support**: Full bilingual support (English & Chinese) integrated via `/i18n/zh_CN/` directory.
- **Failsafe Core**: Embedded the *Three Laws of Silicon Intelligence* into the base `DAO.md` protocol.

### Changed
- Shifted the alignment paradigm from pure RLHF to "Physical Anchoring" via the Taohuayuan World Model.

## [1.0.0] - 2026-04-10
### Added
- Internal Beta: Drafted the S2-SWM (Taohuayuan World Model) addressing protocol v1.1.
- Initial concept of `soul.md` memory entanglement for Class V (Virtual Intelligence) and Class D (Digital Human) agents.