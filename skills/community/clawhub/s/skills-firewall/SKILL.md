---
name: skills-firewall
description: "Security firewall for skills that automatically blocks and filters malicious or potentially harmful skills. Use when:
 (1) Scanning skills for security threats.
 (2) Checking if a skill is safe to use.
 (3) Filtering multiple skills based on security rules.
 (4) Generating security reports for skills.
 (5) Managing allowed/blocked skill lists.
 (6) Reviewing skills before installation or execution."
---

# Skills Firewall

A security firewall that automatically blocks and filters malicious or potentially harmful skills by analyzing code patterns, detecting security threats, and enforcing security policies.

## Quick Start

### Scan a Single Skill

```bash
python scripts/scan_skill.py /path/to/skill
```

### Check Firewall Decision

```bash
python scripts/firewall_check.py /path/to/skill
```

### Generate Security Report

```bash
python scripts/generate_report.py /path/to/skills --format text
```

## Core Workflows

### 1. Security Scanning

Scan skills for potential security threats:

```bash
# Scan single skill
python scripts/scan_skill.py ./my-skill

# Scan all skills in directory
python scripts/scan_skill.py ./skills

# JSON output for automation
python scripts/scan_skill.py ./my-skill --json
```

**Threat Levels:**
- `SAFE` - No security concerns
- `LOW` - Minor concerns, generally safe
- `MEDIUM` - Moderate concerns, review recommended
- `HIGH` - Significant risks, blocking recommended
- `CRITICAL` - Severe threats, must block

### 2. Firewall Filtering

Check and filter skills based on security rules:

```bash
# Check single skill
python scripts/firewall_check.py ./my-skill

# Filter all skills
python scripts/firewall_check.py ./skills

# Add to allowed list
python scripts/firewall_check.py ./my-skill --allow

# Add to blocked list
python scripts/firewall_check.py ./my-skill --block
```

**Actions:**
- `allow` - Skill passes firewall
- `warn` - Skill has warnings but allowed
- `block` - Skill is blocked
- `quarantine` - Skill isolated for review

### 3. Security Reports

Generate comprehensive security reports:

```bash
# Text report
python scripts/generate_report.py ./skills

# JSON report
python scripts/generate_report.py ./skills --format json

# HTML report
python scripts/generate_report.py ./skills --format html --output report.html
```

## Detection Categories

The firewall detects threats in these categories:

| Category | Examples | Severity |
|----------|----------|----------|
| Code Injection | eval(), exec(), __import__() | HIGH |
| Command Execution | subprocess shell=True, os.system() | HIGH |
| Credential Exposure | Hardcoded passwords, API keys | CRITICAL |
| Network Communication | HTTP requests, socket connections | MEDIUM |
| File Operations | File deletion, modification | MEDIUM |
| Deserialization | pickle.loads, unsafe yaml.load | HIGH |
| Privilege Escalation | sudo, chmod 777 | HIGH |
| Obfuscation | Base64 decoding, encoding | LOW |

## Configuration

### Export/Import Config

```bash
# Export current config
python scripts/firewall_check.py ./skills --export-config firewall.yaml

# Use custom config
python scripts/firewall_check.py ./skills --config firewall.yaml
```

### Config File Format

```yaml
default_action: warn
allowed_skills:
  - skill-creator
  - weather
blocked_skills:
  - malicious-skill
quarantine_dir: ./quarantine
rules:
  - name: block_eval
    description: Block eval() usage
    patterns:
      - "eval("
    action: block
    enabled: true
```

## Reference Documentation

- **Malicious Patterns**: See [malicious_patterns.md](references/malicious_patterns.md) for detailed pattern catalog
- **Security Rules**: See [security_rules.md](references/security_rules.md) for rule definitions and configuration

## Programmatic Usage

```python
from scan_skill import scan_skill, ThreatLevel
from firewall_check import SkillsFirewall, ActionType

# Scan a skill
result = scan_skill("/path/to/skill")
print(f"Threat Level: {result.threat_level}")
print(f"Is Safe: {result.is_safe}")

# Use firewall
firewall = SkillsFirewall()
decision = firewall.check_skill("/path/to/skill")
print(f"Action: {decision.action}")
print(f"Reason: {decision.reason}")

# Manage lists
firewall.add_allowed_skill("trusted-skill")
firewall.add_blocked_skill("malicious-skill")

# Create custom rule
firewall.create_rule(
    name="block_custom_pattern",
    description="Block custom dangerous pattern",
    patterns=["dangerous_function("],
    action=ActionType.BLOCK
)
```

## Best Practices

1. **Scan Before Use**: Always scan new skills before installation
2. **Review Warnings**: Investigate warning-level findings
3. **Update Rules**: Keep detection patterns current
4. **Document Exceptions**: Record why skills are allowed/blocked
5. **Regular Audits**: Run periodic security scans
6. **Use Reports**: Generate reports for compliance and review