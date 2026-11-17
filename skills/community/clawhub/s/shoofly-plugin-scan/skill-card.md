## Description:

Pre-install plugin security scanner for OpenClaw plugins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wow-leeroy-jenkins05](https://clawhub.ai/user/wow-leeroy-jenkins05)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan OpenClaw plugin directories for security issues before installation, including credential patterns, obfuscated code, unusual network calls, sensitive path access, and risky exec patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may run the scanner on a plugin directory they did not intend to review or on a release from an untrusted source.

Mitigation: Verify that the skill comes from a trusted source and point it only at plugin directories intended for pre-install review.

Risk: Scan findings and clean results are pre-install review signals and may still require human judgment.

Mitigation: Review reported findings before installation and treat a clean scan as one input in the plugin review process.

## Reference(s):

- [Shoofly Plugin Scan on ClawHub](https://clawhub.ai/wow-leeroy-jenkins05/skills/shoofly-plugin-scan)
- [Publisher profile: wow-leeroy-jenkins05](https://clawhub.ai/user/wow-leeroy-jenkins05)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash command examples and scan result guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes indicate clean results, findings that require review, or scan errors.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
