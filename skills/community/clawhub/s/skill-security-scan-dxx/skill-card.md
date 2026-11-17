## Description:

Scan installed OpenClaw skills for potential security risks. Use when you want to check if skills contain dangerous commands, access sensitive paths, or have other security issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntaffffff](https://clawhub.ai/user/ntaffffff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to run a lightweight local scan of installed OpenClaw skills and review advisory findings about risky commands, sensitive path access, dynamic execution, and network request handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clean scan result can be incomplete because the scanner skips documentation and instruction files.

Mitigation: Treat scanner output as advisory and manually review important skills, including SKILL.md, README, text files, and expected behavior.

Risk: The scanner uses lightweight local pattern matching and may miss unsafe behavior that simple regular expressions do not cover.

Mitigation: Use it as one input in a broader review process and test newly installed skills in an isolated environment before normal use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ntaffffff/skills/skill-security-scan-dxx)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and terminal-style scan report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scanner results are advisory and should be reviewed manually before trusting a skill.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
