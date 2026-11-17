## Description:

Backs up and restores the ~/.openclaw agent folder as encrypted, chunked snapshots stored in a private GitHub repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishbhimani](https://clawhub.ai/user/krishbhimani)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to preserve, migrate, list, and restore their .openclaw agent state through encrypted backups stored in a private GitHub transport repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling and broad git staging could expose or mishandle sensitive or unrelated local data.

Mitigation: Review or fix the skill before routine use, use a fine-grained GitHub token limited to one private backup repository, and verify ~/openclaw-transport and ~/openclaw-transport-temp do not contain unrelated data.

Risk: Restore operations can overwrite local OpenClaw state.

Mitigation: Confirm the intended backup version and current local state before running restore, and treat restore as a potentially destructive operation.

Risk: Setup may install system packages through sudo from an agent-driven workflow.

Mitigation: Avoid running setup.py with sudo from an agent session; install or approve system prerequisites under human supervision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishbhimani/skills/snapshot)
- [GitHub personal access tokens](https://github.com/settings/tokens)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate backup manifests and encrypted snapshot chunks when the bundled scripts are executed.]

## Skill Version(s):

1.2.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
