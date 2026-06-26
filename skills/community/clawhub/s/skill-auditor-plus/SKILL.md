---
name: skill-auditor-plus
description: Security, performance, and quality auditing for AgentSkills. Use when reviewing skills before installation, auditing during development, checking installed skills for risks, optimizing performance, or ensuring best practices compliance. Automated scanning for dangerous operations, credential leaks, token bloat, and quality issues.
---

# Skill Auditor Plus

Transform skill development from "hope it works" to "confidently secure and optimized". This skill provides automated auditing for AgentSkills across three dimensions: security, performance, and quality.

## Why Skill Auditing Matters

- **Security**: Skills run with Codex's permissions - a vulnerable skill can delete files, leak credentials, or execute arbitrary commands
- **Performance**: Large skills consume context window, reducing Codex's effectiveness for the actual task
- **Quality**: Well-structured skills are easier to maintain, more reliable, and provide better user experience

## Core Capabilities

### 1. Security Audit

Automatically scans for:
- **Dangerous operations**: File deletion (`rm -rf`), system commands (`eval`, `exec`), code execution
- **Credential leaks**: Hardcoded API keys, secrets, tokens, passwords
- **Network requests**: External API calls that may be unsafe
- **Suspicious patterns**: Pastebin links, URL shorteners, risky file paths
- **Injection vulnerabilities**: Unsafe user input handling

**Severity levels**:
- 🔴 **High**: File deletion, credential leaks, system command execution
- 🟡 **Medium**: Network requests, code execution, risky file paths
- 🟢 **Low**: Suspicious URLs, file writes

### 2. Performance Audit

Analyzes skill efficiency:
- **Token usage**: Frontmatter (<100 tokens), body (<5000 tokens), line count (<500 lines)
- **Context optimization**: Duplicate content, unreferenced files, large reference files
- **Script efficiency**: Execute permissions, code duplication
- **Recommendations**: Split into references/, use scripts for repeated code

**Key metrics**:
- Frontmatter token count (target: <100)
- Body token count (target: <5000)
- Line count (target: <500)
- Reference file sizes (target: <10k tokens each)

### 3. Quality Audit

Checks best practices compliance:
- **SKILL.md structure**: Proper frontmatter, complete description
- **File organization**: No unnecessary files (README.md, INSTALLATION_GUIDE.md, etc.)
- **Documentation**: Clear usage instructions, examples, error handling
- **Progressive disclosure**: Efficient context loading with references/

## Quick Start

### Audit a skill before installation

```bash
# Clone or download the skill
cd skill-auditor-plus

# Run security audit
python3 scripts/security_audit.py /path/to/skill-to-audit

# Run performance audit
python3 scripts/performance_audit.py /path/to/skill-to-audit
```

### During skill development

```bash
# After making changes, audit your skill
python3 scripts/security_audit.py /path/to/your-skill
python3 scripts/performance_audit.py /path/to/your-skill

# Fix issues, then re-audit
# Iterate until no high/medium severity issues remain
```

### Batch audit installed skills

```bash
# Audit all skills in a directory
for skill in /path/to/skills/*; do
    echo "Auditing $skill"
    python3 scripts/security_audit.py "$skill"
    python3 scripts/performance_audit.py "$skill"
done
```

## Understanding Audit Reports

### Security Audit Report

```json
{
  "total_issues": 5,
  "high_severity": 1,
  "medium_severity": 2,
  "low_severity": 2,
  "issues": [
    {
      "category": "credential_leaks",
      "severity": "high",
      "file": "scripts/api_client.py",
      "line": 15,
      "pattern": "api_key\\s*=\\s*[\"'][\\w-]+[\"']",
      "matched_text": "api_key = \"sk-1234567890\"",
      "context": "api_key = \"sk-1234567890\""
    }
  ]
}
```

**What to do**:
1. Review each issue by severity (high → medium → low)
2. For credential leaks: Use environment variables
3. For dangerous operations: Add warnings or safety checks
4. For network requests: Document purpose and add error handling

### Performance Audit Report

```json
{
  "skill_md_stats": {
    "frontmatter_tokens": 85,
    "body_tokens": 7500,
    "total_tokens": 7585,
    "line_count": 520
  },
  "issues": [
    {
      "severity": "high",
      "category": "body_too_long",
      "message": "Body is too long (7500 tokens, should be < 5000)",
      "suggestion": "Split content into references/ files and link from SKILL.md"
    }
  ]
}
```

**What to do**:
1. **Frontmatter too long**: Move detailed descriptions to body
2. **Body too long**: Split into references/ files, link from SKILL.md
3. **Too many lines**: Break into smaller sections, use references/
4. **Large reference files**: Split further or add grep patterns for searching

## Best Practices

See [best-practices.md](references/best-practices.md) for comprehensive guidelines on:
- Security best practices (credential management, input validation, safe operations)
- Performance optimization (token efficiency, progressive disclosure, script usage)
- Quality standards (documentation, file organization, structure)

## Advanced Usage

### Custom Security Patterns

Edit `scripts/security_audit.py` to add custom patterns:

```python
DANGEROUS_PATTERNS = {
    'custom_risk': [
        r'your_custom_regex_pattern',
    ],
}
```

### Performance Thresholds

Edit `scripts/performance_audit.py` to adjust thresholds:

```python
if stats['body_tokens'] > 5000:  # Change this value
    issues.append({...})
```

### Integration with CI/CD

Add to your CI pipeline:

```yaml
# .github/workflows/skill-audit.yml
name: Skill Audit
on: [push, pull_request]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Security Audit
        run: |
          python3 skill-auditor-plus/scripts/security_audit.py .
      - name: Performance Audit
        run: |
          python3 skill-auditor-plus/scripts/performance_audit.py .
```

## Resources

### scripts/

- **security_audit.py**: Automated security scanning for dangerous operations, credential leaks, and suspicious patterns
- **performance_audit.py**: Performance analysis for token usage, context optimization, and best practices compliance

### references/

- **[best-practices.md](references/best-practices.md)**: Comprehensive guide to AgentSkill development best practices, including security, performance, and quality standards

## Troubleshooting

### "Module not found" errors

Install required dependencies:
```bash
pip install pyyaml  # if needed
```

### False positives in security audit

If the scanner flags safe code:
1. Review the pattern match
2. Add comments explaining why it's safe
3. Consider refactoring to avoid the pattern

### Performance audit shows large body

This is normal for complex skills. Split content into references/:
1. Move detailed sections to references/feature-name.md
2. In SKILL.md, add: "See [FEATURE](references/feature-name.md) for details"
3. Keep only overview and navigation in SKILL.md

## Contributing

Found a bug or want to add features? This skill is open source. Contributions welcome!

## License

MIT License - See LICENSE file for details
