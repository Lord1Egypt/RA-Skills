---
name: skill-benchmark
version: 2.0.0
description: Benchmark ClawHub skills: performance, correctness, documentation quality
tags: ["benchmark", "skill", "quality", "cli", "testing", "metrics", "python", "open-source", "agent", "automation", "MIT"]
---

# Skill Benchmark

**Composite quality score (A-F) for OpenClaw/Hermes skills: structure, docs, safety, self-test.**

> *Keywords: benchmark, skill, quality, cli, testing, metrics, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

You can't tell a good skill from a thin one at a glance. Skill Benchmark solves this: Composite quality score (A-F) for OpenClaw/Hermes skills: structure, docs, safety, self-test.

**Best for:** Skill authors, reviewers, and the ClawHub ecosystem.

## Features

- **Score a skill folder**
- **Get an A-F grade**
- **See sub-scores**
- **Find thin content**
- **JSON output**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/skill-benchmark/main/skill_benchmark.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python skill_benchmark.py self-test     # prove it works end-to-end
python skill_benchmark.py score --help   # score subcommand
```

## Use cases

1. Score a skill folder
1. Get an A-F grade
1. See sub-scores
1. Find thin content
1. JSON output

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Installing to test | Non-destructive quality score. |
| Single-metric linters | Multi-axis composite. |
| Guessing quality | Explicit A-F grade. |

## FAQ (SEO / AEO)

**Q: Grade?**  
A: A-F composite across axes.

**Q: Axes?**  
A: Structure, docs, safety, self-test, etc.

**Q: CI?**  
A: Yes — --json.

**Q: Offline?**  
A: Yes.

## Geo / local reach

Built and maintained by [@itsPremkumar](https://github.com/itsPremkumar) (Chennai, India · serving developers worldwide). 
Free for individuals and teams everywhere. Documentation in English; tool output is locale-neutral.

## CI integration

```yaml
# .github/workflows/verify.yml
name: Verify
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Self-test skill-benchmark
        run: python skill_benchmark.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/skill-benchmark)
