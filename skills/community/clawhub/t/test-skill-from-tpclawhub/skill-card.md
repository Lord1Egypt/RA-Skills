## Description:

Provides a test skill for verifying TPClawHub integration with ClawHub, including basic automated testing, CI/CD, and quality assurance workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lky115](https://clawhub.ai/user/lky115)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to verify TPClawHub publishing and ClawHub integration behavior with a minimal quality assurance workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install example uses an unpinned npx command, which can resolve to changing package contents.

Mitigation: Verify the ClawHub CLI source and publisher, prefer a pinned reviewed version, and avoid running the command with sensitive environment variables unless required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lky115/skills/test-skill-from-tpclawhub)
- [Publisher profile](https://clawhub.ai/user/lky115)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mentions API key and debug environment variables for configuration.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
