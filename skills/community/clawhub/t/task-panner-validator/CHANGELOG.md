# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Features added but not yet released

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security improvements

## [1.0.0] - 2025-02-15

### Added
- Initial release of Task Planner and Validator
- TaskPlanner class for task management
- SafetyValidator for security checks
- TaskExecutor with rollback support
- TaskPlan and Step data models
- Plan persistence (save/load JSON)
- SHA-256 integrity verification
- Dry-run execution mode
- Auto-approve functionality
- Comprehensive logging
- Execution progress tracking
- Checkpoint system for rollbacks
- Dangerous operation detection
- Sensitive path validation
- Multiple step execution modes
- Complete documentation (README, QUICKSTART, API, CONTRIBUTING)
- Example usage file
- Basic test suite
- MIT License

### Features
- ✅ Step-by-step task planning
- 🔒 Built-in security validation
- 🔄 Rollback checkpoint system
- 📝 JSON plan persistence
- 🎨 Integrity checksums
- ⚡ Execution control (dry-run, auto-approve, stop-on-error)
- 📊 Real-time progress tracking
- 🔍 Comprehensive logging
- 🛡️ Dangerous operation detection
- ✨ Zero external dependencies (pure Python)

### Documentation
- Complete README with examples
- Quick start guide (QUICKSTART.md)
- API reference documentation (API.md)
- Contributing guidelines (CONTRIBUTING.md)
- GitHub setup instructions
- Code examples (examples.py)
- Test suite (test_basic.py)

---

## Version History Format

### [X.Y.Z] - YYYY-MM-DD

#### Added
- New features

#### Changed
- Changes in existing functionality

#### Deprecated
- Soon-to-be removed features

#### Removed
- Now removed features

#### Fixed
- Any bug fixes

#### Security
- Security fixes/improvements

---

## Semantic Versioning

Given a version number MAJOR.MINOR.PATCH, increment the:

1. **MAJOR** version when you make incompatible API changes
2. **MINOR** version when you add functionality in a backward compatible manner
3. **PATCH** version when you make backward compatible bug fixes

Examples:
- `1.0.0` → `1.0.1` (bug fix)
- `1.0.1` → `1.1.0` (new feature)
- `1.1.0` → `2.0.0` (breaking change)

---

## Links

- [Repository](https://github.com/cerbug45/task-planner-validator)
- [Issues](https://github.com/cerbug45/task-planner-validator/issues)
- [Releases](https://github.com/cerbug45/task-planner-validator/releases)
