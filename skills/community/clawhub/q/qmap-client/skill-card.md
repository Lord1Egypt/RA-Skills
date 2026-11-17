## Description:

CLI tool for the QuantMap distributed computing protocol. Manages node setup, task execution, and result submission on devnet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chatrichai](https://clawhub.ai/user/chatrichai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and node operators use this skill to install and operate the QMAP CLI for QuantMap devnet wallet setup, worker task execution, validation, coordination, and status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable global npm code and run automatic network tasks.

Mitigation: Review the npm package before installation, pin the package version where possible, and run the CLI in an isolated environment.

Risk: The CLI creates and uses a local devnet wallet identity under ~/.qmap.

Mitigation: Use a disposable devnet identity and keep ~/.qmap out of synced or shared directories.

Risk: Worker task execution may run from an account that can access unrelated files or secrets.

Mitigation: Run worker tasks from a restricted account or sandbox without access to unrelated secrets or important files.

## Reference(s):

- [QMAP Client ClawHub Skill Page](https://clawhub.ai/chatrichai/skills/qmap-client)
- [QMAP Client Homepage](https://clawhub.com/skills/qmap-client)
- [chatrichai Publisher Profile](https://clawhub.ai/user/chatrichai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance focuses on devnet CLI setup, local identity management, task execution, validation, coordination, and status commands.]

## Skill Version(s):

0.1.2 (source: server release evidence and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
