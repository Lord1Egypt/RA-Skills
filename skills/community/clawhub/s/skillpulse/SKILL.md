---
name: skill-profiler
description: Profile offline OpenClaw skill run samples to detect latency, CPU, and memory bottlenecks and compare sessions.
homepage: https://github.com/mike007jd/openclaw-skills/tree/main/skill-profiler
metadata: {"openclaw":{"emoji":"📈","requires":{"bins":["node"]}}}
---

# Skill Profiler

Analyze offline sample sets and surface the slowest or heaviest skills before they become production regressions.

## When to use

- You have JSON sample logs with `latencyMs`, `cpuMs`, and `memoryMb`.
- You want threshold-based hotspot detection for local review or CI.
- You need a shareable JSON or HTML report, or a before/after comparison between two runs.

## Commands

```bash
node {baseDir}/bin/skill-profiler.js run --input ./samples.json
node {baseDir}/bin/skill-profiler.js report --input ./samples.json --out ./report.html
node {baseDir}/bin/skill-profiler.js compare --left ./v1.json --right ./v2.json
```

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

## What it reports

- Average latency and p95 latency per skill
- Average CPU and peak memory per skill
- Bottlenecks using configurable latency, CPU, and memory thresholds
- Session diffs showing added, removed, and changed skills

## Boundaries

- Skill Profiler is built for offline sample analysis, not live tracing.
- It depends on the quality of the input samples and does not capture traces by itself.
