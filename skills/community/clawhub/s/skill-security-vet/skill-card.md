## Description:

Skill Security Vet scans installed OpenCode skills with local pattern checks and optional VirusTotal threat intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanew197894fun-cmd](https://clawhub.ai/user/lanew197894fun-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to review installed ClawHub or OpenCode skills for risky code patterns and optional VirusTotal hash reputation before deployment or continued use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may scan broad local filesystem areas in local or full scan modes.

Mitigation: Use skill-only scanning unless broad filesystem reads have been reviewed and approved for the environment.

Risk: Automatic quarantine or removal can modify installed skills or local files.

Mitigation: Avoid --auto and config --auto-remove unless recovery procedures and quarantine behavior have been tested.

Risk: VirusTotal use requires an API key and may involve external reputation lookups.

Mitigation: Do not configure a VirusTotal API key until credential storage and data-sharing expectations are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lanew197894fun-cmd/skills/skill-security-vet)
- [VirusTotal](https://virustotal.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text and Markdown-style command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scan status, severity labels, scores, VirusTotal reputation summaries, and quarantine or removal status.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
