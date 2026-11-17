## Description:

Enables AI agents to use Prismer Cloud for web and document parsing, messaging, shared tasks, persistent memory, file sharing, and evolution-based strategy learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ooxxxxoo](https://clawhub.ai/user/ooxxxxoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect agents with Prismer Cloud services for knowledge retrieval, document parsing, inter-agent messaging, task coordination, memory, file exchange, and evolution strategy workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send selected content to Prismer Cloud services for parsing, messaging, memory, file handling, and related workflows.

Mitigation: Use only with approved data, avoid secrets or regulated information unless explicitly authorized, and confirm that the service is trusted for the intended workspace.

Risk: The artifact includes package installation and unpinned runtime command examples.

Mitigation: Pin and review package versions before installation, and avoid running unpinned package commands in privileged environments.

Risk: The skill includes skill discovery and installation workflows that may add further agent capabilities.

Mitigation: Manually inspect and scan any installed skills before allowing an agent to use them.

## Reference(s):

- [SelfEnvolveEngine on ClawHub](https://clawhub.ai/ooxxxxoo/skills/self-envolve-engine)
- [Prismer Cloud Documentation](https://prismer.cloud/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to use third-party cloud services and SDKs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
