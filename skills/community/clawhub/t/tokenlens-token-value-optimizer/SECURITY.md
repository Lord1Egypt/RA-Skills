# Security

## Overview

TokenLens Token Value Optimization Engine is designed with security and privacy as first principles.

## Security Claims

### ✅ Verified Security Properties

1. **No Network Calls**
   - All scripts operate locally
   - No external API calls (except OpenClaw's own)
   - No telemetry, no tracking, no analytics

2. **No Code Execution**
   - Scripts do not execute arbitrary code
   - No subprocess calls (except OpenClaw CLI for token tracking)
   - No dynamic code evaluation (eval, exec)

3. **No System Modifications**
   - Scripts do not modify system files
   - All configuration changes are via OpenClaw config API
   - No installation of system packages

4. **Data Local Only**
   - All data stored in `~/.openclaw/workspace/memory/tokenlens/`
   - No data leaves your machine
   - You own 100% of your data

### 🔒 OpenClaw Integration

The skill integrates with OpenClaw through:
- Official OpenClaw CLI (`openclaw session_status`)
- Standard Python scripts
- Local file system only

### 🛡️ Privacy Guarantee

**We cannot see your data because:**
- No network connectivity in scripts
- No external services
- No data collection
- All processing happens on your machine

## Threat Model

The skill is designed to protect against:

1. **Data exfiltration** → No network calls
2. **Unauthorized access** → Local files only
3. **Code injection** → No dynamic execution
4. **System compromise** → No system modifications

## Security Audit

This is version 1.0 of the skill. While we have implemented security best practices, we recommend:

1. Reviewing the source code (all scripts are open)
2. Running in a sandboxed environment if concerned
3. Monitoring file changes in your OpenClaw workspace

## Reporting Security Issues

If you discover a security vulnerability, please:
1. Do not disclose publicly
2. Contact TokenLens security team (security@tokenlens.ai)
3. Provide detailed reproduction steps

We will respond within 48 hours and issue patches as needed.

## Updates

Security updates will be released through standard ClawHub update channels. Always update to the latest version for security fixes.

---

**TokenLens Security Team**  
Last updated: 2026-04-09