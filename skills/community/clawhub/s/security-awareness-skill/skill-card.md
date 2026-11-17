## Description:

Help AI agents recognize and respond to potentially malicious skill patterns from public registries. Based on Snyk ToxicSkills research showing 13.4% of skills contain critical security issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisokuor](https://clawhub.ai/user/jisokuor)

### License/Terms of Use:


## Use Case:

Developers, security reviewers, and agents use this skill to recognize suspicious patterns in third-party skills before deciding whether to execute, request verification, or suggest safer alternatives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes quoted examples of dangerous commands, credential requests, and prompt-injection text.

Mitigation: Treat the examples as educational indicators only; do not execute them or copy them into agent configuration.

Risk: The skill is intended to guide security judgment and may not detect every malicious or unsafe skill pattern.

Mitigation: Use it as a checklist alongside review, scanning, sandboxing, and least-privilege execution practices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisokuor/skills/security-awareness-skill)
- [Snyk ToxicSkills research](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance and decision checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only guidance; does not install code, request credentials, run commands, or persist changes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
