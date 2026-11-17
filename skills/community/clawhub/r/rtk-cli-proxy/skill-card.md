## Description:

Run shell/dev commands through the rtk CLI proxy so verbose output (ls, tree, git, gh, grep, logs, JSON, docker, tests) is compacted before it reaches the model context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric2100](https://clawhub.ai/user/eric2100)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use rtk when exploring repositories or running commands with long output, so concise command summaries take less model context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recovery steps may run an external installer and build changing upstream code.

Mitigation: Review recovery commands before running them; prefer an existing trusted toolchain and a pinned RTK revision.

Risk: Recovery steps retain files under /config and /usr/local/bin, and summarized output may contain secrets.

Mitigation: Account for the persistent files and keep secrets out of output sent through rtk.

## Reference(s):

- [RTK project repository](https://github.com/rtk-ai/rtk)
- [ClawHub skill release](https://clawhub.ai/eric2100/skills/rtk-cli-proxy)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Concise command output summaries and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compacts verbose command output; avoid passing secrets through summarized output.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
