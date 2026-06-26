# Sleep Analyzer v5.3.4

## Overview
Professional EDF sleep analysis skill with accurate security declaration. Provides comprehensive sleep pattern analysis from EDF files.

## SECURITY DECLARATION - ACCURATE
**This skill follows the complete security declaration in SECURITY_STATEMENT.md. All claims are verifiable against the source code.**

### Runtime Security (ACCURATE)
- **Memory storage**: Primary storage in memory during session
- **File writes**: EDF analysis may create temporary files and save charts
- **No runtime network**: No network access during execution
- **Controlled writes**: All file writes restricted to skill directory or user locations

### Installation Security
- **Network required**: Installation needs network for optional dependencies
- **Standard packages**: Only installs from PyPI official sources
- **No binaries**: No binary downloads or installations

## ACCURATE BEHAVIOR DECLARATION

### What This Skill Actually Does:
1. **Reads EDF files** with security restrictions (no path traversal, size limits, file type validation)
2. **Performs sleep analysis** using EDF analysis modules
3. **May create temporary files** for analysis operations (in secure output directory)
4. **May save analysis charts** (plt.savefig) for visualization (in secure output directory)
5. **Stores results in memory** during session
6. **Exports to JSON** with path security checks (no arbitrary file system writes)

### File Security Restrictions:
- **Path traversal protection**: Blocks ".." in file paths
- **Output directory restriction**: All outputs in `analysis_outputs/` directory
- **Export location restriction**: Exports only to current directory or subdirectories
- **File size limits**: Maximum 100MB per EDF file
- **File type validation**: Only EDF/EDF+/BDF/GDF files allowed

## Features

### Core EDF Analysis
- Sleep stage detection and analysis
- Sleep event identification (spindles, K-complexes)
- Respiratory event analysis
- Power spectrum analysis
- All analysis modules included

### Storage & Export
- **Memory storage**: Primary storage during session
- **Analysis outputs**: May be saved to files (charts, data)
- **User-controlled export**: Export to JSON format (user-initiated)
- **Transparent storage**: All storage behavior documented

### Safety Features
- No modification of original EDF files
- Clear separation of analysis and storage
- Accurate behavior declaration
- All file writes documented

## Commands

### `sleep-analyze-store`
Analyze sleep data from EDF file and store results in memory.

```bash
sleep-analyze-store --file <edf_file>
```

**Security**: Read-only input, memory storage, may create analysis files

### `export-result`
Export analysis results to JSON file.

```bash
export-result --id <result_id> --output <output_file>
```

**Security**: User-controlled export to specified location

### `list-results`
List all stored analysis results in memory.

```bash
list-results
```

**Security**: Memory read only, no file access

## Installation

### Basic Installation (Standard Library Only)
```bash
# Copy skill files to OpenClaw skills directory
# Basic functionality works with Python standard library
```

### Advanced Features (Optional Dependencies)
```bash
# Install optional scientific packages
pip install mne numpy scipy matplotlib pandas

# These enable advanced EDF analysis features
# Network required during installation only
```

## Security Verification

### Code Verification
All security claims can be verified by examining the source code:

1. **File writes**: `grep -r "plt\.savefig\|\.to_csv\|open.*w\|os\.makedirs" .`
2. **Network access**: `grep -r "socket\|requests\|urllib" .`
3. **Imports**: Check all import statements

### Testing Recommendations
1. **Sandbox testing**: Run in isolated environment first
2. **File monitoring**: Monitor file system activity
3. **Use non-sensitive data**: Test with sample EDF files

## Support & Documentation

- **Complete security declaration**: SECURITY_STATEMENT.md
- **Version history**: CHANGELOG.md
- **Configuration**: config.yaml
- **Source code**: All Python files included

## Transparency Commitment

This skill follows these transparency principles:

1. **Accurate declaration**: Documentation matches actual code behavior
2. **No hidden functionality**: All features explicitly declared
3. **User awareness**: Users know what files will be created
4. **Verifiable claims**: All security claims can be verified

---
*Sleep Analyzer v5.3.4 - Professional EDF sleep analysis with accurate security declaration*









