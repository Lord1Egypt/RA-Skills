# TIA Hardware Auditor Scripts

## Files
- `TIA-HW-Audit.ps1` - Hardware and I/O audit script

## Usage

```powershell
# Basic usage
.\TIA-HW-Audit.ps1 -FieldBackup "C:\Backups\field\latest.zap18" -MasterBackup "C:\Backups\master\master.zap18" -OutputDir "C:\Reports\audit"

# Weekly audit (called by heartbeat)
.\TIA-HW-Audit.ps1 -FieldBackup "\\nas\factory\field.zap18" -MasterBackup "\\vault\engineering\master.zap18"
```

## Requirements
- Siemens TIA Portal V18 with Openness API
- PowerShell 5.1+
- Read access to both .zap18 files

## Output
- `hardware-diff.csv` - CSV with all changes
- `summary.json` - JSON summary for agent

## CSV Columns
Type, PLC, Rack/Node, Module, OldAddress, NewAddress, OldFW, NewFW, Comment

## Detected Changes
- New/removed PLCs and devices
- I/O address shifts
- Firmware version changes
- Module additions/removals
