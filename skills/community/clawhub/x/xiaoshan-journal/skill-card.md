## Description:

Personal diary automation for OpenClaw that detects configuration, initializes local paths on first run, writes a daily journal from local memory/profile material, and generates a 1080px-wide diary image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1204tmax](https://clawhub.ai/user/1204tmax)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users can use this skill to turn local assistant profile, memory, and optional news summary files into a first-person daily journal entry and a shareable image. It is intended for personal journaling workflows where the user controls the local input paths and output directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads sensitive local OpenClaw profile and memory files.

Mitigation: Review and narrow the configured SOUL, MEMORY, daily memory, and news summary paths before installing or running the skill.

Risk: Generated Markdown, HTML, PNG, and config.yaml files may contain private diary content, names, paths, or preferences.

Mitigation: Treat generated outputs as private and add or verify a .gitignore entry for config.yaml and other private generated artifacts.

Risk: The browser-rendering step processes generated HTML and may run in an environment with uncontrolled active content or network access.

Mitigation: Preview diary content before image rendering and run browser-based rendering only in an environment where network access and active HTML behavior are controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1204tmax/skills/xiaoshan-journal)
- [Artifact README repository link](https://github.com/1204TMax/xiaoshan-journal.git)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, files]

**Output Format:** [Markdown diary text, YAML configuration, generated HTML, and PNG image output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets the previous day using the configured timezone and generates a 1080px-wide image when rendering succeeds.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
