---
name: vibo-skillqa
description: "Test and certify AI agent skills: 7 automated checks, grade A–D, certificate. Use when asked to check, test, review, or certify a skill before publishing. Use ONLY with the user's explicit consent: SkillQA reads the skill folder (incl. .env-like files, for masked secret findings), checks local skill-library metadata for novelty, writes reports locally and a machine-bound license file — tell the user what will be scanned and where reports are saved."
version: 0.2.8
author: Viacheslav Bochkarev
license: Proprietary — https://wwwvibo.com
metadata:
  license_type: cloud-skillqa
  trial: 2 days
  price: "$5/month"
permissions:
  files: [<target-skill-folder>, qa_reports/, ~/.config/skillqa/]
  network: none
  process: [sandboxed skill scripts (env-isolated, network-disabled, hard timeouts)]
---

# ViBo SkillQA

**Local-first. No telemetry, no cloud sync — tested skills and reports never leave your machine.**

Autonomous QA and certification for agent skills (a folder with `SKILL.md`
+ helper scripts). Runs 7 automated checks, grades the skill **A–D** and
issues a certificate you can show to buyers or feed to CI (JSON).

## Commands (run from the skillqa folder)

```bash
python3 skillqa.py test <path-to-skill> [--lang en|ru] [--skip module1,module2] [--load N] [--parallel [N]] [--timeout S]
python3 skillqa.py selftest          # test the tester itself (needs fixtures/ — bundled in the GitHub source repo; marketplace copies omit fixtures)
python3 skillqa.py license --status  # license state (demo vs pro)
```

- **demo**: static scan + teaser report (free, no license needed)
- **pro**: all 7 modules + certificate + JSON for CI (license key, $5/month,
  trial 2 days — https://wwwvibo.com)

## When to use

- User asks to check, test, review, or certify a skill.
- Before publishing a skill to a marketplace — run the check, show the grade.
- After editing a skill — re-run to prove nothing broke.
- **Use only with the user's explicit consent**: testing reads the skill
  folder and executes its scripts in a sandbox. Tell the user what will be
  scanned and where reports are saved before running.

## Privacy, consent, retention & deletion

| What | Where | How to delete |
|---|---|---|
| QA reports (`.md`/`.json`) | `qa_reports/<skill>/` next to the tester | delete the folder |
| License file | `~/.config/skillqa/skillqa_license.dat` | `rm` the file |
| Sandbox copies of the tested skill | temp dir, removed after each run | automatic |

- No telemetry, no cloud sync, no data leaves your machine.
- Reports only store findings (pass/warn/fail, file:line), never secret values
  found inside a tested skill — a leaked secret is reported as a finding, not
  echoed.
- All executables run in a sandbox: fake tokens, no network, hard timeouts.
- Never run a skill's scripts outside the sandbox.

## Permissions

- **Files**: reads the tested skill folder; writes `qa_reports/` and
  `~/.config/skillqa/` only.
- **Process**: sandboxed execution of the tested skill's scripts — including its main script with `--help` under each installed Python interpreter (compat check) — all inside the env-whitelisted, network-disabled, timeout-killed sandbox. Never as the calling agent.
- **Network**: none (sandbox runs with network disabled).
- **Secrets**: never read, logged or sent; only flagged as a finding.

## License (important!)

This skill is **commercial**. Demo mode is free (static scan + teaser report);
full certification (7 modules, grade, certificate, JSON) requires a valid
ViBo SkillQA license — see https://wwwvibo.com. The registry listing carries
the platform default license (MIT-0) which covers the hosted showcase copy
only; the product itself is licensed per the terms above.
