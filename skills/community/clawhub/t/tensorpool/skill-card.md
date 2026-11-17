## Description:

This skill helps users migrate local machine learning scripts to TensorPool GPU clusters using the interactive cluster workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tycho-svoboda](https://clawhub.ai/user/tycho-svoboda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare local machine learning training or inference scripts for TensorPool GPU clusters, transfer code, run GPU jobs, retrieve outputs, and clean up resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project files or sensitive credentials could be transferred to TensorPool during migration.

Mitigation: Review transfer scope and rsync excludes before upload; do not transfer .env files, API tokens, private keys, regulated data, or proprietary datasets unless an approved secure method is in place.

Risk: The skill may edit and rerun user code while diagnosing migration failures.

Mitigation: Require confirmation before code edits, package installation, file transfer, cluster creation, cluster destruction, or other irreversible or billable actions.

Risk: TensorPool CLI behavior may differ from examples in the skill text.

Mitigation: Use a pinned TensorPool CLI install where possible and discover the current tp command syntax with --help before executing TensorPool commands.

## Reference(s):

- [TensorPool Docs](https://docs.tensorpool.dev)
- [Cluster Quickstart](https://docs.tensorpool.dev/clusters-quickstart)
- [Instance Types](https://docs.tensorpool.dev/resources/instance-types)
- [CLI Reference](https://docs.tensorpool.dev/cli/overview)
- [ClawHub Skill Page](https://clawhub.ai/tycho-svoboda/skills/tensorpool)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and code or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dependency setup, file-transfer commands, TensorPool cluster lifecycle steps, and scoped code edits for migration errors.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
