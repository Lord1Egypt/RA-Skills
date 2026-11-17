# sluice

An outbound **egress guard**. Every message an agent sends — an email, a social
draft, a Telegram reply, a write to the public site — passes through a gate that
scans it for leaked secrets and private identifiers, and either refuses it or
redacts them in place.

Agents touch live credentials all day: API keys in `.env`, bot tokens in systemd
units, JWTs from Supabase. One careless paste into outbound copy and a key is on
the public internet forever. `sluice` is the sluice gate between the machine's
insides and the outside world.

Pure stdlib. No network, no model call, no dependencies.

## Usage

```bash
# gate a draft before it goes out — only sends if clean
sluice scan draft.md && ./send-it draft.md

# scrub a file and keep going
sluice redact draft.md > safe.md

# sits in a pipe
generate-post | sluice redact | queue-to-typefully

# machine-readable
sluice scan --json draft.md
```

`scan` prints findings to **stderr** and exits non-zero when it sees a breach at
or above `--fail-on` (default `high`), so it drops straight into a `&&` chain or
a pre-send hook. `redact` writes cleaned text to **stdout**.

## What it catches

**High severity** (live credentials — block by default):
Anthropic / OpenAI / OpenRouter keys, GitLab & GitHub PATs, AWS access keys,
Slack tokens, Stripe live keys, Telegram bot tokens, JWTs / Supabase keys,
PEM private-key blocks.

**Medium** (probable secret / internal disclosure):
`key = <high-entropy value>` assignments (gated on Shannon entropy so prose
doesn't trip it), private infrastructure paths.

**Low** (topology leak): RFC1918 private IPs.

Previews never echo the full secret — `glpa…z9 (26 chars)`, never the value.

## Precision first

A guard that cries wolf gets switched off. Every high-severity detector is tuned
to fire only on shapes that are almost certainly the real thing; the generic
`key=value` rule carries an entropy gate. Measured on this machine's real
outbound corpus (122 published articles + queued drafts, 1.36M characters):

- **Recall:** 14/14 (100%) on planted, realistically-shaped secrets.
- **False positives:** 0 high, 2 medium across 1.36M chars — and both mediums
  were genuine internal-path disclosures sitting in already-published copy, not
  false alarms.

Reproduce: `python3 bench.py`.

## Extending

Add a `Detector` to the list in `sluice/detectors.py`: a name, severity, a
compiled regex, a redaction label, and an optional second-stage validator
(e.g. an entropy floor or a checksum) for lower-confidence shapes.

## Tests

```bash
python3 -m unittest discover -s tests
```

39 stdlib unit tests: every detector, overlap resolution, redaction,
entropy gating, and the CLI exit-code contract.
