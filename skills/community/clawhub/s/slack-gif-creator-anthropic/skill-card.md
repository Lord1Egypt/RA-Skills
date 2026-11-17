## Description:

Knowledge and utilities for creating animated GIFs optimized for Slack, including constraints, validation tools, and animation concepts for Slack GIF requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupuking723](https://clawhub.ai/user/pupuking723)

### License/Terms of Use:

Apache 2.0

## Use Case:

External users and developers use this skill to create Slack-ready animated GIFs, including emoji-style animations, by following Slack constraints and using bundled Python helper utilities to build, optimize, and validate GIF files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency hygiene and image-parser exposure when installing Python packages or processing untrusted image files.

Mitigation: Install in an isolated Python environment as a normal user, pin dependencies with hashes or a lockfile for higher-assurance use, and be cautious with untrusted image files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pupuking723/skills/slack-gif-creator-anthropic)
- [Skill source](artifact/SKILL.md)
- [Python dependencies](artifact/requirements.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local GIF files when the agent uses the bundled Python helpers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
