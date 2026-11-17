## Description:

Guides agents through Tinker CLI, SDK, and cookbook workflows for training runs, checkpoints, fine-tuning recipes, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjrwtx](https://clawhub.ai/user/zjrwtx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML engineers use this skill to manage Tinker training runs and checkpoints, run SFT and RL cookbook recipes, and troubleshoot Tinker CLI or SDK workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags mutable package upgrades and broad activation behavior.

Mitigation: Pin package versions or run setup in an isolated environment, and review proposed install or upgrade commands before execution.

Risk: The security guidance notes possible API key exposure through diagnostics.

Mitigation: Avoid printing API keys and prefer ephemeral credentials or restrictive permissions on ~/.tinker/config.json.

Risk: The security summary flags public or destructive checkpoint operations.

Mitigation: Require explicit confirmation before deleting checkpoints, publishing checkpoints, or pushing artifacts to public repositories.

## Reference(s):

- [Tinker CLI Reference](references/cli-reference.md)
- [Tinker Cookbook Recipe Deep-Dives](references/cookbook-recipes.md)
- [Tinker Troubleshooting Guide](references/troubleshooting.md)
- [Tinker SDK](https://github.com/thinking-machines-lab/tinker)
- [Tinker Cookbook](https://github.com/thinking-machines-lab/tinker-cookbook)
- [Skill Source Repository](https://github.com/zjrwtx/max_skills)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose package installation, credential configuration, checkpoint management, and Hugging Face publishing steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
