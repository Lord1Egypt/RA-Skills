# Changelog

All notable changes to the WoL Wakeup skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-23

### Added
- Initial release of WoL Wakeup skill
- Support for Wake-on-LAN device management
- Workflow mode for multi-turn conversations
- Single-line command mode for quick operations
- Keyword-based triggering without AI model dependency
- Device persistence in `~/.openclaw/wol/devices.json`
- Session state management for workflow conversations
- HTTP Hook service for OpenClaw Internal Hooks integration
- Systemd service configuration for auto-start
- Installation script with dependency checking
- Comprehensive documentation (README, USAGE, INTEGRATION_GUIDE)

### Features
- List saved WoL devices
- Add new devices via workflow or single-line command
- Wake devices by name or index number
- Remove devices from saved list
- Timeout handling for workflow sessions
- Health check endpoint for monitoring

### Technical
- Python 3 required
- Depends on `wakeonlan` pip package
- OpenClaw Internal Hooks integration
- Configurable HTTP endpoint (default: port 8765)

---

## Future Versions (Planned)

- [ ] Support for multiple network interfaces
- [ ] Scheduled wake-up tasks
- [ ] Device status polling (if supported by hardware)
- [ ] Web UI for device management
- [ ] Mobile app integration
