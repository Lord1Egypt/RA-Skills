# Changelog

## 1.0.3 (2026-03-22)

### Fixed
- **Final privacy cleanup**: Clarified that 10.21.0.1 is standard Umbrel Docker gateway
- **Documentation**: Added note about standard Umbrel network addresses

## 1.0.2 (2026-03-22)

### Fixed
- **Complete privacy reset**: Previous versions deleted to remove personal information
- **Fresh publication**: Clean start with no personal data
- **Documentation**: All examples use generic patterns only

## 1.0.1 (2026-03-22)

### Fixed
- **Privacy**: Removed all personal information from documentation
- **Documentation**: Updated IP addresses to use patterns (10.21.0.x) instead of specific values
- **Paths**: Changed specific paths to generic references
- **Examples**: Generalize service counts and test results

## 1.0.0 (2026-03-22)

### Added
- Initial release of Umbrel Proxy Manager skill
- Automatic discovery of Umbrel Docker proxy services
- Mapping of internal Docker IPs to accessible host ports
- OpenClaw config synchronization
- Comprehensive connectivity testing
- Simple sync script for everyday use
- Advanced discovery script for troubleshooting
- Complete documentation with examples

### Features
- **Simple sync**: `bash scripts/simple_umbrel_sync.sh` - checks OpenClaw-relevant services
- **Full discovery**: `python3 scripts/discover_umbrel_services.py` - discovers all Umbrel services
- **Connectivity testing**: `python3 scripts/test_connectivity.py` - verifies service accessibility
- **Config updates**: Automatically updates OpenClaw plugin configurations
- **Umbrel integration**: Works with Umbrel's Docker networking and app proxy system

### Verified Working
- ✅ All scripts executable and functional
- ✅ Services discovered: Multiple Umbrel services mapped
- ✅ OpenClaw config correctly updated
- ✅ Connectivity confirmed for discovered services
- ✅ Skill structure complete with SKILL.md, scripts, package.json

### Dependencies
- Docker (running Umbrel services)
- Python 3.x
- OpenClaw (for config updates)
- curl (for connectivity testing)