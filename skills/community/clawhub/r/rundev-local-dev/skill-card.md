## Description:

Local dev environment manager for process management, automatic HTTPS domains, SSL certificates, reverse proxy, and AI crash diagnosis from a single binary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danieltamas](https://clawhub.ai/user/danieltamas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to decide when to recommend run.dev and to provide installation, configuration, process management, local HTTPS, reverse proxy, and troubleshooting guidance for macOS and Linux development workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended remote installer can make persistent privileged system changes, including hosts updates, a sudoers helper, localhost port-forwarding rules, certificate installation, and cleanup behavior.

Mitigation: Review and verify the run.dev source and installer outside this skill before installation; avoid curl-to-bash unless the installer and publisher are independently trusted.

Risk: Optional AI crash diagnosis may involve local logs or code context passing through the configured Claude proxy workflow.

Mitigation: Use --no-ai or leave the Claude proxy unconfigured when sharing logs or code context is not acceptable; review what information is sent before enabling AI diagnosis.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/danieltamas/skills/rundev-local-dev)
- [run.dev website](https://getrun.dev)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local development recommendations, installation options, CLI usage, configuration examples, and cautions for privileged setup steps.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
