---
name: arabic-threat-intel
slug: arabic-threat-intel
display_name: "Arabic Threat Intelligence — استخبارات المصادر المفتوحة"
version: 1.0.0
author: neo-kw
license: MIT
tags:
  - osint
  - threat-intelligence
  - arabic
  - cybersecurity
  - telegram
  - dark-web
  - apt
  - middle-east
  - incident-response
validation:
  tested_on: "OpenClaw 2026.3.13"
  requires_tools:
    - exec
    - read
    - write
  no_api_key_required: true
  optional:
    - tor (for dark web search)
changelog:
  - version: "1.0.0"
    date: "2026-03-18"
    changes:
      - "Initial release"
      - "Arabic Telegram channel OSINT monitoring"
      - "Bilingual Arabic/English threat report generation"
      - "Dark web search via Tor"
      - "CT log passive subdomain discovery"
      - "Iran-linked APT group tracking"
description: "The only Arabic-first OSINT and threat intelligence skill. Monitor Arabic-language threat actor channels on Telegram, generate bilingual threat reports, search the dark web via Tor, and enumerate subdomains via Certificate Transparency logs. Works for any region — Middle East, Africa, Asia, or global. No API keys required."
argument-hint: "<channel|report|darkweb|scan> [target] [--lang ar|en|both] [--region all|me|africa|asia]"
---

# Arabic Threat Intelligence

The **only Arabic-first** OSINT and threat intelligence skill for OpenClaw. Works globally — not limited to any single country or region.

## Why This Skill

99% of OSINT skills are English-only. Arabic-speaking analysts, security teams, and researchers lack native-language tooling. This skill bridges that gap with full bilingual (Arabic + English) support.

## Commands

### Monitor Telegram Channels
```
Use arabic-threat-intel channel hak994
Use arabic-threat-intel channel anyChannelName --lang both
```
Scrapes public Telegram channels. Returns posts with timestamps, auto-translates Hebrew/Farsi mentions.

### Generate Threat Report
```
Use arabic-threat-intel report "critical infrastructure"
Use arabic-threat-intel report "ransomware" --lang both
```
Monitors tracked threat actor channels and generates a structured bilingual threat brief ready for leadership or SOC teams.

### Dark Web Search
```
Use arabic-threat-intel darkweb "company name data leak"
Use arabic-threat-intel darkweb "اسم الشركة تسريب"
```
Searches dark web indexes via Tor. Accepts Arabic or English queries. Returns .onion links with risk assessment.

### CT Log Subdomain Scan
```
Use arabic-threat-intel scan example.com
Use arabic-threat-intel scan target-domain.org
```
Passive subdomain discovery via Certificate Transparency logs (crt.sh). Flags takeover candidates, dev/test servers, VPN and admin panels.

## Tracked Threat Groups

| Group | Platform | Origin | Targeting |
|-------|----------|--------|-----------|
| Fatimion Cyber Team | Telegram @hak994 | Iran | Infrastructure, Oil & Gas |
| 313 Team | Telegram @xX313XxTeam | Iran | Government sites |
| Fattah Cyber | Telegram @fattah_irili | Iran | Tech, Media |
| Handala Hack | Web | Iran (MOIS) | Financial, Defense |
| Various APT34/MuddyWater | Multiple | Iran | Telecom, Energy |

## Output Options

| Flag | Description |
|------|-------------|
| `--lang ar` | Arabic only (RTL output) |
| `--lang en` | English only |
| `--lang both` | Bilingual report (default) |
| `--region me` | Middle East focus |
| `--region africa` | Africa focus |
| `--region all` | Global (default) |

## Requirements
- **No API keys required** for CT log scanning and Telegram monitoring
- **Optional:** Tor for dark web search (`service tor start`)
- Python 3.10+ (pre-installed with OpenClaw)

## Use Cases
- 🔒 SOC teams monitoring Arabic-language threat actors
- 🕵️ OSINT investigators tracking dark web activity
- 📰 Journalists covering cybersecurity in the Middle East
- 🎓 Security researchers and students learning Arabic OSINT
- 🏢 Enterprise security teams with MENA exposure
- 🌍 Any analyst tracking Iran-linked APT groups globally

## Security & Ethics
This skill performs **passive OSINT only**. All sources are publicly accessible:
- Telegram public channels (t.me/s/)
- Certificate Transparency logs (crt.sh)
- Dark web search engines via Tor (Ahmia, OnionLand)

No active exploitation. No unauthorized scanning.
