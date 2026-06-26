---
name: self-skill-evolver
description: Analyze and improve OpenClaw agent skills by tracking usage, checking skill health, scanning code quality, and generating actionable improvement suggestions. Use when evaluating skill reliability, performance, maintainability, or release readiness.
---

# Self Skill Evolver

A Python CLI tool for analyzing and improving OpenClaw agent skills.

## Features

- usage monitoring
- skill health scoring
- SKILL.md and code analysis
- automated improvement suggestions
- JSON / Markdown / HTML reporting

## Installation

```bash
clawhub install self-skill-evolver
```

## Typical Commands

```bash
self-skill-evolver init
self-skill-evolver analyze <skill-name>
self-skill-evolver analyze --all
self-skill-evolver report <skill-name>
self-skill-evolver report --all
self-skill-evolver health <skill-name>
self-skill-evolver health --all
self-skill-evolver log <skill-name> <action> --status success --duration 100
self-skill-evolver feedback <skill-name> 5 --comment "Very helpful"
self-skill-evolver clear --days 90
self-skill-evolver log --list
```

## Dependencies

- Python 3.8+
- SQLite3
- PyYAML
- GitPython (optional)
