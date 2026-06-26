# Windows Screenshot - OpenClaw Skill

A pure PowerShell screenshot tool using GDI+ for Windows systems.

## Quick Start

```powershell
# Run directly
powershell -File screenshot.ps1

# Or via OpenClaw
openclaw exec powershell -File screenshot.ps1
```

## Environment Variables

- `OPENCLAW_MEDIA_DIR` - Custom output directory (optional)
  - Default: `$USERPROFILE\.openclaw\media`
  - Script creates directory automatically if needed

## Files

- **screenshot.txt** - PowerShell script (rename to .ps1 if needed)
- **SKILL.md** - Skill documentation and metadata
- **README.md** - This file

## Source Code

All code is open source and available on GitHub for review:
https://github.com/vvxer/windows-screenshot

## License

MIT-0 (Free to use, modify, and redistribute without attribution)

