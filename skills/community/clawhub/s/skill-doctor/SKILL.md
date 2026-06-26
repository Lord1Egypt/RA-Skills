---
name: skill-doctor
description: "Diagnoses the health of your published ClawHub skills and plugins, then prescribes concrete next actions. Use when: (1) User asks how their skill/plugin is performing, (2) User wants to know which of their published items needs attention, (3) User asks for growth advice on a ClawHub listing, (4) User wants a portfolio-wide check-up across all their skills and plugins, (5) User mentions stalled downloads, low install conversion, a pending/suspicious moderation verdict, or a stale version. Works standalone with rule-based diagnostics, or with an Anthropic API key for deeper narrative analysis."
tags: [clawhub, analytics, diagnostics, monitoring, python, dashboard, growth]
license: MIT
version: 1.0.3
metadata:
---

# Skill Doctor

A check-up for your ClawHub portfolio. Skill Doctor pulls live data for every skill and plugin you own via `clawhub inspect` / `clawhub package inspect`, runs it through a rule-based diagnostic engine, and hands you a prioritized prescription: what's healthy, what's at risk, and what to do about it this week.

Think of it as a doctor's visit for your published work — vitals in, diagnosis out.

## Why this exists

Tools like `clawhub-monitor-all.sh` (or any cron-based watcher) tell you **what changed**. Skill Doctor tells you **what it means** — whether a number is good, bad, or needs context, and what the highest-leverage next step is.

## First-Use Initialisation

Before running a check-up, verify the `clawhub` CLI is installed and authenticated:

```bash
command -v clawhub >/dev/null 2>&1 || { echo "clawhub CLI not found — install it first"; exit 1; }
```

Confirm a config directory exists for storing diagnostic history (used for trend detection across runs):

```bash
mkdir -p ~/.skill-doctor
[ -f ~/.skill-doctor/config.json ] || echo '{"slugs":[],"plugins":[],"anthropic_api_key":null}' > ~/.skill-doctor/config.json
```

Never overwrite an existing config. Ask the user which slugs/plugins to track on first run if the config is empty.

## Quick Reference

| Situation | Action |
|-----------|--------|
| First run, no config | Ask user for their skill slugs and plugin names, save to `~/.skill-doctor/config.json` |
| User asks "how's my skill doing?" | Run `scripts/checkup.py --slug <name>` |
| User asks for full portfolio review | Run `scripts/checkup.py --all` |
| User wants deeper analysis, has an API key | Run `scripts/checkup.py --all --deep` |
| User wants a visual trend | Run `scripts/checkup.py --all --chart` |
| Verdict is `suspicious` or `malware` | Treat as **critical** — surface immediately, do not wait for scheduled run |
| Download-to-install ratio is low | Flag as `conversion` issue, suggest description/positioning review |
| Version is stale (>90 days, no changes) | Flag as `staleness` issue |
| No prior state on file | First-time baseline only — do not report deltas, just current standing |

## Running a Check-Up

### Single skill

```bash
python3 scripts/checkup.py --slug proof-of-contribution
```

### Full portfolio (all configured skills + plugins)

```bash
python3 scripts/checkup.py --all
```

### With AI-narrated analysis (optional, requires API key)

```bash
python3 scripts/checkup.py --all --deep
```

This sends the structured diagnostic (not raw secrets) to the Anthropic API for a short narrative summary and prioritized recommendation. It is **opt-in** — never send data to the API unless `--deep` is explicitly passed and a key is configured.

### With a trend chart

```bash
python3 scripts/checkup.py --all --chart
```

Outputs a PNG to `~/.skill-doctor/charts/` showing downloads/installs over time per skill, using locally stored history — no new API calls.

## Diagnostic Categories

Skill Doctor groups every finding into one of these, mirroring how a real check-up triages issues:

| Category | Meaning | Example Finding |
|----------|---------|------------------|
| `vitals` | Core health signals | Downloads, installs, active installs, stars |
| `moderation` | Trust/safety status | `clean`, `pending`, `suspicious`, `malware` |
| `conversion` | Funnel efficiency | Downloads high but installs low — description/positioning issue |
| `staleness` | Maintenance signal | No version bump in N days while downloads keep growing |
| `momentum` | Trend direction | Accelerating, flat, or declining vs. prior check |
| `risk` | Anything urgent | Suspicious verdict, malware flag, sudden drop in active installs |

## Severity Levels

| Severity | Meaning | Response |
|----------|---------|----------|
| `critical` | Trust/safety issue or active-install collapse | Surface immediately, suggest action same day |
| `warning` | Conversion or staleness issue | Include in next scheduled report |
| `info` | Healthy, positive trend, or no action needed | Note only, no action required |

## Output Format

Each check-up produces one prescription block per skill/plugin:

```markdown
## 🩺 <Display Name> (<slug>)

**Status**: healthy | needs-attention | critical
**Verdict**: clean | pending | suspicious | malware

### Vitals
- Downloads: X (Δ since last check: +Y)
- Installs (all-time): X
- Active installs: X
- Stars: X

### Findings
- [severity] Finding description

### Prescription
1. Concrete, specific next action
2. Concrete, specific next action

---
```

## Rule-Based Diagnostic Logic

These are deterministic checks Skill Doctor always runs, no API key required. See `references/diagnostic-rules.md` for the full rule set and exact thresholds — summarized here:

- **Conversion check**: installs / downloads ratio below a configurable threshold → flag `conversion`
- **Staleness check**: days since last version bump vs. days since last download growth → flag `staleness`
- **Momentum check**: compare current vitals to last stored snapshot → `accelerating` / `flat` / `declining`
- **Trust check**: any verdict other than `clean` → flag `moderation`, severity scales with verdict
- **Active-install drop check**: active installs falling while all-time installs stays flat → flag `risk`

## Deep Analysis (Optional, API-Powered)

When `--deep` is passed and `~/.skill-doctor/config.json` has a valid `anthropic_api_key`:

1. Build a compact JSON summary of all findings (no raw tokens, no secrets — just metrics and rule outputs)
2. Send to Claude via the Messages API with a prompt asking for a short prioritized narrative
3. Present the narrative above the rule-based prescriptions, clearly labeled as AI commentary

If no key is configured, skip this step silently and rely on rule-based output only — never block the core check-up on missing AI access.

See `references/deep-analysis-setup.md` for API key configuration.

## State & History

Each run stores a snapshot per slug at `~/.skill-doctor/state/<slug>.json` so the next run can compute deltas and momentum. This mirrors the state-file pattern used by shell-based ClawHub watchers, but in structured JSON for easier analysis and charting.

Do not log API keys, tokens, or full `clawhub inspect` payloads beyond what's needed for the metrics above.

## Publishing Your Own Findings as a Skill

If a diagnostic pattern proves broadly useful (e.g., a new rule that catches a real issue across many users' skills), it can be proposed as an addition to `references/diagnostic-rules.md` rather than hardcoded per-user — keep the core engine generic so it works for anyone's ClawHub portfolio, not just one project.

## Support This Skill

If Skill Doctor saved you time, consider sending a few sats:

⚡ Lightning: `welove@blink.sv`

## Best Practices

1. **Run before publishing changes** — establish a baseline so the next check-up shows real impact
2. **Treat `critical` findings as same-day items** — moderation issues affect trust immediately
3. **Don't chase every metric** — focus the prescription on the 1-2 highest-leverage actions
4. **Re-run after acting** — confirm the fix moved the needle before considering it resolved
5. **Keep `--deep` opt-in** — rule-based diagnostics should never depend on network/API availability
