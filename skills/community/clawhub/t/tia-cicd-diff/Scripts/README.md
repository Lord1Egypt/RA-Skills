# TIA Openness Diff Scripts

## Files
- `TIA-Openness-Diff.ps1` - Main diff script

## Usage

```powershell
# Basic usage
.\TIA-Openness-Diff.ps1 -Baseline "C:\Projects\baseline.zap18" -New "C:\Projects\new.zap18" -Output "C:\Projects\diff-result.json"

# With absolute paths
.\TIA-Openness-Diff.ps1 -Baseline "\\nas\engineering\baseline.zap18" -New "\\nas\field\latest.zap18"
```

## Requirements
- Siemens TIA Portal V18 with Openness API installed
- PowerShell 5.1+
- Read access to .zap18 files

## Output
Returns JSON with:
- Summary (counts of added/removed/modified FBs, DBs)
- Detailed list of changes with descriptions
- Timestamp and file paths

## Notes
- The script extracts .zap18 (ZIP format) to temp directory
- Compares XML/SCL file contents
- Detects added, removed, and modified blocks
- Safe to run multiple times (cleans up temp dirs)
