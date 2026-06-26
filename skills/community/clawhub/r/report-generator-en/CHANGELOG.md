# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2026-03-27

### Security
- Removed unicode control character (Zero Width Joiner U+200D) from HR section emoji
  - Changed "🧑‍💼" to "👤" to eliminate prompt-injection vector
  - File now passes security scanning for hidden/control characters

## [1.0.0] - Initial Release

### Added
- Initial release of Report Generator EN
- Comprehensive template library for 10+ role types:
  - Generic Engineering Weekly Report
  - Executive / Management Weekly Report
  - Team Weekly Report
  - Sales Weekly Report
  - Marketing Weekly Report
  - Project Status Report
  - HR Weekly Report
  - Operations Weekly Report
  - Finance Weekly Report
- Support for multiple output formats (standard, compact, executive)
- Multi-language support via `/lang` command
- No-fabrication policy and quality checklist
- Writing principles and best practices guide
- Quick prompts for minimal, standard, and detailed modes
