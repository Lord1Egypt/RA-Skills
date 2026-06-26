# Self Skill Evolver

Python CLI tool for analyzing and optimizing OpenClaw Agent Skills.

## Overview

Self Skill Evolver helps you:
- **Monitor Usage** - Track calls, success rates, response times
- **Assess Health** - Composite scoring system to identify issues
- **Analyze Code Quality** - Check SKILL.md completeness, syntax, style
- **Generate Recommendations** - Auto-suggest improvements
- **Export Reports** - JSON, Markdown, HTML formats

## Quick Start

```bash
# Install via clawhub (recommended)
clawhub install self-skill-evolver

# Or clone manually
git clone https://github.com/openclaw/skills/self-skill-evolver.git
cd self-skill-evolver
pip install -r requirements.txt
```

### Initialize

```bash
# Initialize database
self-skill-evolver init
```

### Basic Usage

```bash
# Analyze a skill
self-skill-evolver analyze my-skill

# Generate health report
skill-envolve report my-skill

# View all skills health
self-skill-evolver health --all
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize database |
| `analyze` | Analyze skill code |
| `report` | Generate health report |
| `health` | View health scores |
| `log` | Log skill usage |
| `feedback` | Add user feedback |
| `clear` | Clear old data |

## Health Scoring

Composite score based on:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Reliability | 30% | Based on success rate |
| Performance | 20% | Based on response time |
| Code Quality | 30% | Based on code analysis |
| User Satisfaction | 20% | Based on feedback |

### Status Levels

- 🟢 **healthy** (≥80) - Running well
- 🟡 **warning** (60-79) - Needs improvement
- 🔴 **critical** (<60) - Has serious issues

## Python API

```python
from skill_evolver import SkillMonitor, SkillAnalyzer, SkillReporter

# Monitor
monitor = SkillMonitor()
with monitor.track("my-skill", "process") as tracker:
    result = do_work()

# Analyze
analyzer = SkillAnalyzer()
result = analyzer.analyze_skill("my-skill")
print(f"Score: {result.score}/100")

# Report
reporter = SkillReporter()
report = reporter.generate_health_report("my-skill")
print(f"Health: {report['overall_score']}")
```

## Requirements

- Python 3.8+
- SQLite3 (built-in)
- PyYAML, GitPython (optional)

## License

MIT License