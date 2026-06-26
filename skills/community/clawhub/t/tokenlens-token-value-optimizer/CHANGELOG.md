# Changelog

All notable changes to the TokenLens Token Value Optimization Engine will be documented in this file.

## [1.0.3] - 2026-04-09

### Fixed
- **CLI usability**: `optimize.sh` now shows help and exits cleanly when called without arguments
- **Empty prompt handling**: `context_optimizer.py` gracefully shows help for empty prompts
- **Engineering robustness**: All scripts pass comprehensive test suite (28 tests)

### Improvements
- Better user experience: clear help messages, intuitive error handling
- Consistent behavior across all CLI entry points
- Enhanced test coverage for edge cases

## [1.0.2] - 2026-04-09

### Fixed
- **Documentation accuracy**: Updated support links from placeholder "coming soon" to accurate "planned for Q2 2026" statements
- **Community information**: Added ClawHub skill page as current support channel
- **Factual claims**: Removed misleading references to non-existent documentation/community resources

### Documentation
- README.md: Support section now accurately reflects current availability
- SKILL.md: Support & Community section updated for transparency
- All references to tokenlens.ai/docs changed to reflect planning status

## [1.0.1] - 2026-04-09

### Fixed
- **Security compliance**: Removed subprocess usage to match security claims
- **ClawHub flag resolution**: Internal consistency between SKILL.md security metadata and actual script behavior
- **Token tracking**: Now uses only historical/mock data (no external command execution)
- **Data source**: Updated reporting to reflect actual data sources

### Technical
- Removed `subprocess` import and real-time OpenCLaw CLI calls
- Updated `.clawhubsafe` integrity hashes
- Verified all security claims are accurate:
  - `scripts_no_subprocess: true`
  - `scripts_no_code_execution: true`
  - `scripts_no_network: true`
  - `scripts_data_local_only: true`

## [1.0.0] - 2026-04-09

### Added
- Initial release of TokenLens Token Value Optimization Engine
- Core token tracking with daily/weekly aggregation
- Efficiency scoring (1-10 scale)
- Smart optimization recommendations:
  - Context loading optimization
  - Model selection suggestions
  - Heartbeat interval tuning
  - Session pruning reminders
- Context optimizer with prompt analysis
- Model router with tier-based recommendations
- Unified CLI (`optimize.sh`) for all operations
- Local data storage (no external calls)
- Comprehensive documentation

### Features
- **Token tracking**: Record and analyze token usage
- **Value scoring**: Calculate efficiency scores
- **Recommendations**: Personalized optimization suggestions
- **Context optimization**: Load only necessary files
- **Model routing**: Match models to task complexity
- **Reporting**: Weekly optimization reports
- **Privacy**: 100% local, no telemetry

### Technical Details
- Python-based scripts (no external dependencies)
- OpenClaw-native integration
- Works with all OpenClaw versions 2026.2.15+
- Compatible with all major model providers

---

**TokenLens — "Every token, fully seen."**