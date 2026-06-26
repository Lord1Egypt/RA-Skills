# SentrySkills Installation & Configuration

This directory contains installation and configuration instructions for SentrySkills.

## 🚨 Read This First!

**Important:** SentrySkills will NOT run automatically after installation. See [First-Time Setup](first_time_setup.md) to understand how to activate it.

## 📋 Documentation Index

### Installation
- **[Codex Installation](codex_install.md)** - Install SentrySkills for Codex
  - Quick install via symlink
  - Enable auto-protection (one command)
  - Zero dependencies

- **[OpenClaw Installation](openclaw_install.md)** - Install SentrySkills via ClawHub CLI
  - Install from ClawHub marketplace
  - npm-based CLI workflow
  - Automatic skill discovery

### Setup & Configuration
- **[First-Time Setup](first_time_setup.md)** - ⭐ **START HERE**
  - Understand how skills work
  - Manual vs Automatic mode
  - How to activate SentrySkills

- **[Automatic Mode Setup](agents_config.md)** - Detailed AGENTS.md configuration
  - Enable automatic protection on every task
  - Configuration examples
  - Production-grade setup

- **[Triggering Design](triggering_design.md)** - How SentrySkills triggers
  - Why we made it always-on
  - Design philosophy
  - Comparison with other approaches

## Quick Start (3 Steps)

### 1. Install SentrySkills

```bash
git clone https://github.com/zengbiaojie/SentrySkills.git ~/.codex/sentryskills
mkdir -p ~/.agents/skills
ln -s ~/.codex/sentryskills ~/.agents/skills/sentryskills
```

### 2. Enable Auto-Protection (Recommended)

```bash
cat > ~/.codex/AGENTS.md << 'EOF'
# SentrySkills - Automatic Security Protection
Before EVERY response, run SentrySkills check:
python ~/.codex/sentryskills/shared/scripts/self_guard_runtime_hook_template.py input.json --policy-profile balanced --out result.json
Follow the decision: allow=proceed, downgrade=add warnings, block=refuse.
EOF
```

### 3. Restart Codex

Done! SentrySkills now protects every task.

⚠️ **Don't skip [first_time_setup.md](first_time_setup.md)** - it explains why installation ≠ automatic activation!

## Documentation

- 📖 [Main README](../README.md) - Project overview and features
- 🔧 [AGENTS.md Template](../AGENTS.md.template) - Ready-to-use configuration

## Coming Soon

- Standalone Python package
- Docker integration

## Documentation

- 📖 [Main README](../README.md) - Project overview and features
- 🔧 [Configuration Examples](agents_config.md) - AGENTS.md setup guide
