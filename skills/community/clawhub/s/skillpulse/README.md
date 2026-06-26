# Skill Profiler

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> A focused profiling CLI for OpenClaw skill runs that turns raw sample logs into bottleneck reports.

| Item | Value |
| --- | --- |
| Package | `@mike007jd/openclaw-skill-profiler` |
| Runtime | Node.js 18+ |
| Interface | CLI + JavaScript module |
| Main commands | `run`, `report`, `compare` |

## Why this exists

OpenClaw workflows often look healthy until one skill starts stretching tail latency, CPU time, or memory usage. Skill Profiler gives you a compact way to analyze sample traces, apply thresholds, and compare two sessions before a regression reaches production.

## What it does

- Aggregates `latencyMs`, `cpuMs`, and `memoryMb` from JSON sample arrays
- Calculates average latency, p95 latency, average CPU, and peak memory per skill
- Flags bottlenecks with configurable latency, CPU, and memory thresholds
- Exports JSON or HTML reports for sharing and review
- Compares two profiling sessions to highlight added, removed, and changed skills

## Primary workflow

1. Collect run samples into a JSON array.
2. Run `skill-profiler run` to detect hotspots.
3. Export a JSON or HTML report with `skill-profiler report`.
4. Compare before/after snapshots with `skill-profiler compare`.

## Quick start

```bash
git clone https://github.com/mike007jd/openclaw-skills.git
cd openclaw-skills/skill-profiler
npm install
node ./bin/skill-profiler.js run --input ./fixtures/samples-a.json
```

## Commands

| Command | Purpose |
| --- | --- |
| `skill-profiler run --input <samples.json>` | Analyze one sample set and return `0` or `2` depending on bottlenecks |
| `skill-profiler report --input <samples.json> --out <file>` | Export a JSON or HTML report |
| `skill-profiler compare --left <samples.json> --right <samples.json>` | Compare two profiling snapshots |

## Sample input

```json
[
  {
    "sessionId": "s1",
    "skill": "clawshield",
    "latencyMs": 1320,
    "cpuMs": 910,
    "memoryMb": 240
  }
]
```

## What the output tells you

- `run` prints a summary table or JSON envelope and exits with code `2` when thresholds are exceeded
- `report` writes a reusable artifact for dashboards, handoffs, or incident review
- `compare` highlights regressions, improvements, and newly added or removed skills

## Project layout

```text
skill-profiler/
├── bin/
├── fixtures/
├── src/
├── test.js
└── SKILL.md
```

## Status

The current implementation is optimized for offline sample analysis rather than live tracing. It already covers threshold-based bottleneck detection, report export, and session comparison.
