# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-19

### Added
- Initial release of Smart Skill Finder
- Multi-ecosystem skill discovery (Skills CLI, Clawhub, GitHub)
- Smart query understanding using OpenClaw's semantic capabilities
- Relevance ranking and security status reporting
- Graceful degradation when ecosystems are unavailable
- Comprehensive documentation (SKILL.md, README.md, examples.md)
- Configuration support via config.json
- Proper error handling and timeout protection

### Security Features
- Read-only operation (never executes installation commands)
- Security status display from ecosystem scanners
- Controlled subprocess usage with input sanitization
- No access to sensitive user files or credentials
- Proper timeout limits for all external calls

### Publishing Ready
- MIT License included
- Complete documentation suite
- Examples covering common use cases and edge scenarios
- Integration patterns with other OpenClaw skills
- Best practices and troubleshooting guidance
- Renamed from "Intelligent Skill Finder" to "Smart Skill Finder" for better branding and discoverability