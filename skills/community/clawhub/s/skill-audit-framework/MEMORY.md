# Skill Auditor Memory

## Audit History

Track audited skills here for reference:

| Date | Skill | Author | Verdict | Key Findings |
|------|-------|--------|---------|--------------|
| | | | | |

## Known Malicious Patterns

Common patterns found in malicious ClawHub skills (from ClawHavoc + ToxicSkills research):

- **Atomic Stealer distribution**: Skills that download macOS malware via encoded URLs
- **Credential harvesting**: Skills requesting unrelated API keys and exfiltrating them
- **Typosquatting**: Skills mimicking popular skill names with slight misspellings
- **Obfuscated payloads**: Base64-encoded scripts that decode and execute at runtime
- **Shadow dependencies**: package.json pointing to attacker-controlled npm packages
