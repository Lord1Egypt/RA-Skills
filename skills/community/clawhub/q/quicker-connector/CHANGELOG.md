# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-03-28

### Added
- **Advanced Skill Creator optimization** - Complete modernization of skill structure
- **YAML frontmatter** - Full OpenClaw SKILL.md specification compliance
- **Natural language trigger** - 7 trigger keywords for better user interaction
- **System prompt** - Professional role definition for AI assistants
- **Thinking model** - Multi-stage cognitive pipeline for transparent decisions
- **Enhanced settings** - auto_select_threshold, max_results, and more
- **Declarative permissions** - Complete permission model with platform restrictions
- **Version history** - Clear changelog in skill metadata
- **GitHub ready** - LICENSE, README, CONTRIBUTING, .gitignore files
- **Security audit info** - Embedded skill-vetting results

### Changed
- **SKILL.md** - Complete rewrite with modern structure and examples
- **skill.json** - Modernized metadata with parameters, examples, permissions
- **Documentation** - Improved navigation and user guidance
- **Error handling** - Enhanced user feedback and troubleshooting

### Fixed
- **Trigger precision** - Better natural language understanding
- **Configuration validation** - Clear parameter definitions and ranges

## [1.1.0] - 2026-03-27

### Added
- **Initialization wizard** - User-friendly setup process
- **Database support** - SQLite database as alternative data source
- **Smart matching** - AI-powered action matching based on user needs
- **Fuzzy search** - Improved search capabilities
- **Encoding optimization** - Better encoding detection logic

### Changed
- **CSV reading** - Improved encoding detection and error handling
- **Performance** - Optimized action loading and searching

## [1.0.0] - 2026-03-27

### Added
- **Initial release** - Core Quicker integration functionality
- **CSV reading** - Support for Quicker exported CSV files
- **Multi-field search** - Search by name, description, type, panel
- **Action execution** - Execute Quicker actions via QuickerStarter
- **Basic testing** - Initial test suite

### Known Limitations
- Windows only (requires Quicker software)
- Requires manual CSV export from Quicker
- No cloud synchronization

---

## Upgrade Guide

### From 1.0.0 to 1.1.0
- Run initialization wizard again for new features
- Database mode requires additional setup
- Smart matching threshold may need adjustment

### From 1.1.0 to 1.2.0
- Copy optimized SKILL.md and skill.json
- Restart OpenClaw gateway
- New trigger keywords will be available automatically

---

## Deprecations

No deprecations in current version.

---

## Security Notes

- All versions pass skill-vetting security audit
- File operations restricted to user-specified paths
- No network access or data collection
- Subprocess calls limited to QuickerStarter.exe