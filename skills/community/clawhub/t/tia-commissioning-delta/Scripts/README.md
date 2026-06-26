# TIA Commissioning Delta Scripts

## Files
- `TIA-Commissioning-Delta.ps1` - Process control focused diff

## Usage

```powershell
# Compare yesterday vs latest site backup
.\TIA-Commissioning-Delta.ps1 -Baseline "C:\Backups\yesterday.zap18" -New "C:\Backups\latest.zap18" -Output "C:\Reports\delta.json"
```

## Requirements
- Siemens TIA Portal V18 with Openness API
- PowerShell 5.1+

## Focus Areas
1. **Safety Blocks** - E-STOP, safety interlocks, SIL/PL logic
2. **PID Controllers** - Control parameters, tuning
3. **Sequences** - Step logic, state machines
4. **Alarms** - HMI alarms, warnings, faults

## Risk Levels
- CRITICAL: Safety bypasses, interlocks disabled
- HIGH: Safety changes, sequence removal
- MEDIUM: PID tuning, alarm changes
- LOW: Minor modifications

## Output
JSON with:
- Summary counts
- List of changes with risk levels
- Block names and descriptions
