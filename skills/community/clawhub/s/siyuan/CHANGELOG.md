# Changelog

All notable changes to this project will be documented in this file.

## [1.0.3] - 2026-03-20

### Changed
- Updated ClawHub display name to "SiYuan Note" (install name remains "siyuan")

## [1.0.2] - 2026-03-20

### Fixed
- Display name formatting on ClawHub

## [1.0.1] - 2026-03-20

### Fixed
- Removed unnecessary `curl` from required binaries (uses urllib)
- Fixed config path mismatch: now correctly looks for `skills/siyuan/config.yaml`
- Verified no dangerous unicode control characters (UTF-8 Chinese characters are normal)

## [1.0.0] - 2026-03-20

### Added
- Complete API client with automatic retry and error handling
- 8 CLI tools for common operations (list, read, search, create, delete, update, move, export)
- Full notebook management (create, open, close, rename, remove)
- Document operations (create, read, update, move, export as Markdown)
- Block-level editing (insert, update, delete, move)
- SQL query support for advanced search
- Asset upload (images, attachments)
- Configuration file support (config.yaml)
- Comprehensive documentation (SKILL.md, README.md)
- Bilingual documentation (Chinese/English)

### Security
- API token stored in config.yaml (not included in repository)
- Config template provided (config.example.yaml)

## [0.5.0] - 2026-03-18

### Added
- Initial release
- Basic API client
- Core CLI tools
