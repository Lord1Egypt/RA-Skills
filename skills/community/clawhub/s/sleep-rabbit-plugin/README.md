# Sleep Analyzer v5.3.4

A transparent sleep analysis skill for OpenClaw with memory-first storage.

## Quick Start

```bash
# Install the skill
openclaw skill install sleep-analyzer

# Analyze sleep data
sleep-analyze-store --file sleep_data.edf

# Export results
export-result --id <result_id> --output results.json

# List stored results
list-results
```

## Security Overview

**This skill follows the complete security declaration in SECURITY_STATEMENT.md.**

### Key Security Points:
- ‚ú?**Memory storage**: Results stored only in memory during session
- ‚ö†Ô∏è **Optional logging**: Logging disabled by default for security
- ‚ù?**No runtime network**: No network access during execution
- ‚ú?**Transparent behavior**: All actions clearly declared

### File Operations:
- **Reads**: User-provided EDF files (analysis only)
- **Writes**: Optional logs and user-initiated exports only
- **Location**: Skill directory only (no system access)

## Features

### Core Analysis
- Sleep stage detection (NREM, REM, Wake)
- Sleep event identification
- Respiratory pattern analysis
- Power spectrum analysis

### Storage
- **Memory-first**: All results in memory (session lifetime)
- **Export option**: Manual export to JSON format
- **No persistence**: No automatic file writes

### Safety
- Read-only analysis of input files
- No modification of original data
- Clear separation of concerns
- Transparent operation

## Commands

### `sleep-analyze-store`
Analyze EDF file and store results in memory.

**Usage:**
```bash
sleep-analyze-store --file <path_to_edf>
```

**Security:** Read-only file access, memory storage

### `export-result`
Export specific analysis result to JSON file.

**Usage:**
```bash
export-result --id <result_id> --output <json_file>
```

**Security:** User-initiated, explicit file location

### `list-results`
List all analysis results in memory.

**Usage:**
```bash
list-results
```

**Security:** Memory read-only

## Installation

### Basic Installation
```bash
openclaw skill install sleep-analyzer
```

### Optional Dependencies
For advanced analysis features (EEG/MEG analysis):
```bash
pip install mne numpy scipy
```

**Note:** Network required only during installation for optional dependencies.

## Configuration

Default settings (safe configuration):
```yaml
logging:
  enabled: false  # Logging disabled by default
  
storage:
  primary: "memory"  # Memory storage only
  
security:
  runtime:
    network_access: "none"  # No runtime network
```

## Security Verification

### Code Verification
```bash
# Check for file writes
grep -r "open.*w" skill.py

# Check for network access
grep -r "requests\|http\|socket" skill.py

# Check for system calls
grep -r "subprocess\|os.system" skill.py
```

### Runtime Monitoring
1. Use file system monitoring tools
2. Monitor network traffic
3. Check process permissions

## Troubleshooting

### Common Issues

**"No module named mne"**
- Install optional dependencies: `pip install mne numpy scipy`
- Or use basic analysis features only

**"File not found"**
- Ensure EDF file exists
- Check file permissions

**"Memory full"**
- Export results to free memory
- Restart session to clear memory

### Performance Tips
- Use smaller EDF files for faster analysis
- Export results regularly to manage memory
- Disable logging for better performance

## Development

### Code Structure
```
skill.py              # Main skill implementation
config.yaml           # Configuration (matches security declaration)
SKILL.md              # Documentation (references security declaration)
SECURITY_STATEMENT.md # Complete security declaration
```

### Security Principles
1. **Transparency**: All behavior clearly declared
2. **Consistency**: All documents match security declaration
3. **Safety**: Default safe configuration
4. **Control**: User controls risky operations

## Support

### Documentation
- `SKILL.md`: Complete skill documentation
- `SECURITY_STATEMENT.md`: Security declaration
- `config.yaml`: Configuration details

### Issues
Report issues with:
1. Skill version
2. Environment details
3. Steps to reproduce
4. Expected vs actual behavior

### Security Reports
Report security concerns to maintainers with:
1. Detailed vulnerability description
2. Reproduction steps
3. Suggested fix

## License
MIT License - See LICENSE file for details.

---

**All documentation consistently references SECURITY_STATEMENT.md. Report any inconsistencies immediately.**












