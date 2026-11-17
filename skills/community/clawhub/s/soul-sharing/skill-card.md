## Description:

Give AI agents persistent identity and shared memory across runtimes, devices, and sessions — Git-native, no database, no vendor lock-in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingcharleslzy-ai](https://clawhub.ai/user/kingcharleslzy-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up Git-backed identity and memory that can persist across agent runtimes, devices, and sessions. It is intended for users who deliberately want durable shared memory across multiple agents or machines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may persist sensitive or unwanted long-term memories to a shared GitHub repository.

Mitigation: Use only a private repository with restricted access, require user approval before committing memories, and avoid storing secrets, regulated data, raw conversations, or confidential project details.

Risk: The workflow depends on mutable external template files and scripts.

Mitigation: Review and pin the external repository and scripts before installation or deployment.

Risk: GitHub Actions or repository automation may run in the memory repository.

Mitigation: Consider disabling GitHub Actions unless the automation has been reviewed and is required.

## Reference(s):

- [Soul Sharing ClawHub page](https://clawhub.ai/kingcharleslzy-ai/skills/soul-sharing)
- [agent-soul template repository](https://github.com/kingcharleslzy-ai/agent-soul)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git and python3.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
