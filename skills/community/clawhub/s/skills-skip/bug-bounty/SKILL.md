---
name: bug-bounty
description: |
  🐛 Professional Bug Bounty Hunting with AI
  
  AI-assisted bug bounty hunting. Recon to report.
  Web2 + Web3 vulnerabilities.
  
  Features:
  - Recon automation
  - IDOR, XSS, SSRF detection
  - OAuth & GraphQL testing
  - LLM injection detection
  - Web3 smart contract auditing
  - Report generation
  
  Platforms: HackerOne, Bugcrowd, Intigriti, Immunefi
  
  Use when: user wants to find bugs, security testing, or code audit.
  
metadata:
  openclaw:
    emoji: 🐛
---

# 🐛 Bug Bounty Hunter

## Quick Start

```bash
cd /root/.openclaw/workspace/skills/bug-bounty

# Run CVE hunter
python3 cve_hunter.py --target example.com

# Use agents for specialized hunting
ls agents/

# Generate report
python3 report.py --findings findings.json
```

## Vulnerability Classes

### Web2 (18 classes)
- IDOR, XSS, SSRF, CSRF
- OAuth misconfigurations
- GraphQL vulnerabilities
- SQL Injection
- Race conditions
- Business logic flaws

### Web3 (10 classes)
- Re-entrancy
- Integer overflow
- Access control
- Flash loan attacks
- Price oracle manipulation
- Unchecked external calls

## Tools Available

| Tool | Purpose |
|------|---------|
| cve_hunter.py | CVE scanner |
| agents/ | Specialized agents |
| commands/ | Slash commands |

## Note

This is a GitHub repo, not a pure SKILL.md skill.
Run directly from: /root/.openclaw/workspace/skills/bug-bounty/
