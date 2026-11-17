## Description:

Skill Cortex helps OpenClaw agents find, install, use, learn from, and discard temporary skills from ClawHub or GitHub when installed skills cannot complete a task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ankwu001](https://clawhub.ai/user/ankwu001)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to add a temporary capability layer that searches for relevant skills, requests approval, executes selected skills, learns task-routing signals, and cleans up cached skills afterward.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search for, install, execute, and uninstall third-party skills, including unreviewed GitHub-sourced skills when ClawHub results are insufficient.

Mitigation: Require explicit approval before each installation and candidate switch, and manually inspect unreviewed packages before use.

Risk: Reflex mode can skip execution-plan confirmation for frequently successful read-only skills.

Mitigation: Disable or avoid reflex mode unless the version, read-only side effects, and success history are verified.

Risk: The local cortex file stores task-routing signals and skill history.

Mitigation: Keep entity filtering enabled, store only abstract signals, and review cortex.json contents and permissions when tasks involve sensitive data.

## Reference(s):

- [Skill Cortex on ClawHub](https://clawhub.ai/ankwu001/skills/skill-cortex)
- [OpenClaw](https://github.com/openclaw)
- [ClawHub](https://clawhub.ai)
- [Design Document](artifact/DESIGN.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local cortex.json state and propose temporary skill installation or uninstallation with user approval.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
