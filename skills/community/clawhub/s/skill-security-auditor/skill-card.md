## Description:

Command-line security analyzer for ClawHub skills. Run analyze-skill.sh to scan SKILL.md files for malicious patterns, credential leaks, and C2 infrastructure before installation. Includes threat intelligence database with 20+ detection patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akhmittra](https://clawhub.ai/user/akhmittra)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and security reviewers use this skill to run local, pattern-based checks on ClawHub skills before installation or during skill due diligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overstate confidence because its security verdicts come from lightweight pattern matching.

Mitigation: Treat results as advisory, review the full skill package and dependencies, and combine the report with manual review and external scanning.

Risk: Installation guidance asks users to make a shell script executable and optionally add a persistent shell alias.

Mitigation: Review the script and pattern database before chmod, use pinned installer versions, and skip the shell alias unless persistent shortcut behavior is desired.

Risk: A SAFE result may miss novel or sophisticated malicious behavior outside the bundled pattern database.

Mitigation: Do not rely on a clean result alone; inspect scripts, dependencies, network behavior, and ClawHub scan data before installing high-impact skills.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/akhmittra/skills/skill-security-auditor)
- [README](artifact/README.md)
- [Pattern Database](artifact/patterns/malicious-patterns.json)
- [ClawHavoc Campaign Reference](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)
- [OpenClaw Vulnerabilities Reference](https://www.scworld.com/brief/reports-shed-light-on-more-openclaw-vulnerabilities)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal text and Markdown-style audit reports with risk scores, findings, positive indicators, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis is heuristic and depends on the bundled JSON pattern database and local command-line tools.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
