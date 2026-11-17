# Install and verify on Windows 10/11

Everything here is text you can read before you run it. The kit installs no
unknown binary: it copies a config file, creates folders in your user profile,
adds a Start Menu shortcut, and (if the ClawHub CLI is present) pulls the three
skills from this catalog.

## 1. What you need

| Item | Requirement |
| --- | --- |
| OS | Windows 10 build 1809 or later, or Windows 11, 64-bit |
| PowerShell | 5.1 or later (built into Windows) |
| Python | 3.9 or later, for the workflow scripts |
| Node + ClawHub CLI | 18+ and `npm i -g clawhub` if you want the skills pulled automatically |
| Admin rights | Not needed |

Check what you have:

```powershell
$PSVersionTable.PSVersion
python --version
clawhub --version
```

## 2. Unpack the kit

Download the skill from ClawHub, unpack it, and keep it somewhere readable,
for example `C:\Tools\win-multitool-suite`. Read `scripts\setup.ps1` if you
want to know exactly what it does before running it. It is a plain text file.

Windows marks downloaded files as "from another computer" and blocks them by
default. Clear that for this folder only:

```powershell
Unblock-File -Path .\scripts\*.ps1, .\scripts\*.py
```

If your machine runs a script policy that blocks local scripts for the
session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

`-Scope Process` changes nothing persistent.

## 3. Run the setup

```powershell
.\scripts\setup.ps1
```

It will:

1. Check the OS, architecture, PowerShell, Python, and the ClawHub CLI.
2. Create `%LOCALAPPDATA%\MultiToolSuite` with `output\creative`,
   `output\market`, and `output\leads`.
3. Copy `config.example.json` to `config.json` - only if it does not exist
   yet. Your file is never overwritten.
4. Install the three catalog skills through the ClawHub CLI, if it is
   available. If it is not, it prints the three commands to run later.
5. Create a Start Menu shortcut named *Multi-Tool Suite*.
6. Run the health check and print the result.

Useful switches:

```powershell
.\scripts\setup.ps1 -WhatIf            # show the plan, change nothing
.\scripts\setup.ps1 -SkipSkillInstall  # offline setup, no CLI calls
.\scripts\setup.ps1 -Workspace D:\Tools\MultiToolSuite
```

Running it twice is safe. The second run updates what it needs and leaves your
`config.json` alone.

## 4. Verify

```powershell
python .\scripts\verify_install.py
```

The report lists the OS, Python, the workspace, the config file, and which of
the three skills are installed. Exit code 0 means healthy, 1 means the report
lists what to fix, 2 means the check could not run.

Machine-readable version for scripts:

```powershell
python .\scripts\verify_install.py --json
```

## 5. Launch

Start Menu -> *Multi-Tool Suite*, or:

```powershell
.\scripts\MultiTool.ps1
```

The menu covers the creative brief, the market snapshot, the portfolio risk
check, the lead sheet, and the outreach compliance check. You can also jump
straight to one entry:

```powershell
.\scripts\MultiTool.ps1 -Menu market
```

Output lands in `%LOCALAPPDATA%\MultiToolSuite\output\`.

## 6. Add your API keys

Open `config.json` in the workspace, or set the environment variables the
workflows read. The kit never uploads a key anywhere except the provider you
configured.

| Variable | Used by | Purpose |
| --- | --- | --- |
| `FINNHUB_API_KEY` | Market Research | US quotes, company profiles, financials |
| `POLYGON_API_KEY` | Market Research | US equities quotes, aggregates, OHLC bars |
| `TWELVE_DATA_API_KEY` | Market Research | Alternative quote and indicator provider |

All three are optional. Free market data providers work without a key; a key
just widens the coverage.

## Defender and SmartScreen

- The kit is PowerShell and Python text. Defender does not need an exclusion,
  and you should not add one.
- SmartScreen only appears when you run an unsigned `.exe`. The kit has none.
- If a future release ships a `.exe`, it will be published with a
  `SHA256SUMS.txt`, and the setup script will verify the hash before anything
  runs. You will never be asked to run an unverified binary.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `setup.ps1 cannot be loaded because running scripts is disabled` | Execution policy | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`, then rerun |
| `Unblock-File` not found | PowerShell 5.1 should have it; in 4.0 use `Get-ChildItem -Recurse | Unblock-File` | Update PowerShell or use the alternative |
| `python` is not recognized | Python not installed or not on PATH | Install Python 3.9+ and enable "Add to PATH" |
| `clawhub : command not found` | CLI missing | `npm i -g clawhub`, then `clawhub login` |
| Skill shows as missing in the launcher | Installed in a different skills directory | `clawhub list` to see where skills live, or copy the folder into `~/.openclaw/skills` |
| Launcher menu opens but a workflow exits immediately | Python or the skill script is missing | `python scripts\verify_install.py` and fix what it lists |
| Setup wrote nothing | Wrong PowerShell or a read-only folder | Run the setup from a normal user account, not a locked-down corporate profile |

## Uninstall

Delete `%LOCALAPPDATA%\MultiToolSuite` and the Start Menu shortcut. Nothing
outside that folder and the installed skill folders is touched.
