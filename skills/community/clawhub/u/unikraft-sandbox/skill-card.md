## Description:

Run agent tasks inside an isolated Unikraft Cloud (UKC) sandbox VM for untrusted code, script testing, build reproduction, or other work that should not execute on the host.

This skill is ready for commercial/non-commercial use.

## Publisher:

[procub3r](https://clawhub.ai/user/procub3r)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to provision, operate, synchronize files with, execute commands in, and tear down an isolated UKC sandbox VM for tasks that should be separated from the host workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe path and local state handling may affect user files or expose sandbox credentials.

Mitigation: Use only trusted sandbox names and non-sensitive workspaces until the scripts validate names and store state in a private directory.

Risk: SSH host identity is not verified for sandbox connections.

Mitigation: Avoid sensitive credentials or data until host identity verification is added for SSH and rsync operations.

Risk: Local-to-sandbox synchronization uses destructive deletion in the sandbox workspace.

Mitigation: Review the local directory before syncing and treat the sandbox workspace as disposable unless destructive sync controls are added.

## Reference(s):

- [UKC API Reference](references/ukc_api.md)
- [ClawHub skill page](https://clawhub.ai/procub3r/skills/unikraft-sandbox)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell and Node.js command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UKC_TOKEN, UKC_METRO, UKC_USER, and UKC_SANDBOX_IMAGE environment variables.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
