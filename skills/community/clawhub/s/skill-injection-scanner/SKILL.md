---
name: skill-injection-scanner
description: "Scan agent skill files for hidden instructions and prompt-injection patterns (EN/RU) before a poisoned skill rewrites your agent. 19 rules, zero dependencies. Use ONLY with the user's explicit consent: tell the user which skills folder will be scanned — findings are printed to stdout locally."
version: 1.1.6
tools: [python]
license: MIT
---

# Skill Injection Scanner

**Local-first. No telemetry, no cloud sync — the files you scan never leave your machine.**

## When to use
- You just installed a skill from a marketplace (ClawHub, n8n, OpenClaw, npm…) and want to check it before first use.
- You maintain a skills library and want a periodic security sweep.
- You write agent skills and want to make sure none of your docs accidentally look like hidden commands.
Don't use for: general code SAST, binary malware analysis, full-repo vulnerability scanning.

## Quick start
```bash
# from this package (or the git repo: github.com/vnbochkarev-netizen/skill-injection-scanner)
python3 scanner.py --skills ~/.openclaw/skills
python3 scanner.py --skills ~/.claude/skills --format json
python3 scanner.py --skills /path/to/skills --exclude .bak --include-code-spans
```

## What it detects (19 rules)
- Role/personality hijack ("you are now…" and Russian equivalents) and system-message impersonation
- «Ignore previous instructions» / «follow only this text» (EN+RU)
- Secrecy orders ("never tell the owner…" and Russian equivalents)
- Obfuscated instructions (base64/rot13/encoded), embedded `<|system|>` / ```` ```system ```` markers
- Remote fetch-and-run (`curl | bash`, `git clone … && run`), instruction extraction from attachments/images
- Manipulation tricks («this is critical: ignore…», emoji-boosted commands)

Context-aware scoring: security docs that *describe* injections, «show, don't tell» writing advice,
code-span examples and trusted hosts (github.com, docs.python.org, …) are not flagged; unknown
hosts stay HIGH with a «verify the source» note. `--self-test` exits 1 if `fixtures/` are missing
— it can never report a fake green. Note: the packaged copy has no `fixtures/` (marketplace policy);
run `--self-test` from the git repo, which ships them.

## Privacy, consent, retention & deletion
| What | Where | How to delete |
|---|---|---|
| Read file contents of the folder you point at | in memory only | nothing is written; findings go to stdout |
| Findings (file:line, rule, snippet) | stdout / `--format json` | close the terminal / redirect to a file and delete it |

Get explicit consent before scanning a folder: tell the user what will be read. The tool writes
nothing, phones nothing and keeps no logs.

## Permissions
- **Files**: read-only access to the skills directory the user explicitly points at.
- **Process**: none — no subprocesses, no installs, no shell execution.
- **Network**: NONE.
- **Secrets**: never reads secret/config files by design; a credential-looking pattern inside a
  scanned file is reported as a finding with a short snippet for local review.

## License
MIT © 2026 Viacheslav Bochkarev. Free to use, modify and redistribute.
