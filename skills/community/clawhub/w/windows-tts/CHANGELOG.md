# Changelog

All notable changes to the windows-tts skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-15

### Added
- Initial release of windows-tts skill
- 4 core tools:
  - `tts_notify` - Send text notifications to Windows Azure TTS
  - `tts_get_status` - Check TTS server connection status
  - `tts_list_voices` - List available Azure TTS voices
  - `tts_set_volume` - Set default volume level
- HTTP client with timeout and error handling
- TypeScript type definitions
- Comprehensive configuration validation
- Full documentation in SKILL.md

### Features
- Cross-device TTS broadcast over LAN
- Support for all Azure TTS voices
- Configurable default voice and volume
- Safe guards for volume and timeout settings
- Compatible with OpenClaw plugin architecture

### Technical
- Built with TypeScript
- Zero runtime dependencies
- Uses native fetch API
- Compiled to ES2020 compatible JavaScript
