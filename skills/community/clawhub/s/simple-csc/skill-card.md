## Description:

Use the simple-csc repository to perform Chinese Spelling Correction and Chinese Character Error Correction with large language models in a training-free workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacob-zhou](https://clawhub.ai/user/jacob-zhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up and operate the simple-csc repository for Chinese spelling correction, C2EC experiments, LMCorrector API usage, local API serving, and evaluation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to run unpinned third-party setup scripts and dependencies that were not included in the reviewed artifact.

Mitigation: Review the upstream repository and scripts before execution, use a pinned commit and pinned package versions, and run in an isolated environment without production credentials or broad host filesystem access.

Risk: Correction requests may contain sensitive text sent to a local API or model server.

Mitigation: Avoid sending sensitive text unless you control the running model and server environment.

## Reference(s):

- [Simple CSC ClawHub release page](https://clawhub.ai/jacob-zhou/skills/simple-csc)
- [simple-csc repository](https://github.com/Jacob-Zhou/simple-csc)
- [Simple CSC detailed reference](references/details.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, shell, JSON, YAML, and curl examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local setup commands, API request examples, corrected text examples, and evaluation output descriptions.]

## Skill Version(s):

1.0.1 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
