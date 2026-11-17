## Description:

Run Alibaba Cloud Qwen Code CLI via background process for task execution, code review, and automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[userb1ank](https://clawhub.ai/user/userb1ank)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to run Qwen Code CLI workflows for coding tasks, code review, headless automation, and CI/CD-oriented analysis from an agent environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill promotes unattended Qwen CLI runs that may change code or project files.

Mitigation: Run it from an isolated workspace, review generated changes before merging, and avoid -y/--yolo or automated approvals on important code.

Risk: The helper wrapper can execute unintended shell commands or create persistent skill files outside the intended location.

Mitigation: Do not pass untrusted values to mcp, extensions, or skill create until the wrapper is fixed, and restrict use to trusted projects.

Risk: Using @latest for the Qwen CLI can introduce unreviewed upstream behavior changes.

Mitigation: Pin the Qwen CLI version and update only after review.

## Reference(s):

- [Qwen Code Official Docs](https://qwenlm.github.io/qwen-code-docs/zh/)
- [Qwen CLI Command Reference](references/qwen-cli-commands.md)
- [Example Code](assets/examples/)
- [Qwen Code Skill Repository](https://github.com/UserB1ank/qwen-code-skill)
- [ClawHub Skill Page](https://clawhub.ai/userb1ank/skills/qwen-code-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON output from headless Qwen runs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Qwen CLI, Node.js 20 or later, network access, and either OAuth or API key authentication.]

## Skill Version(s):

1.2.0 (source: server release metadata and changelog, released 2026-02-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
