## Description:

Generates Xiaohongshu-style content drafts and a semi-automated local publishing page with copy, content switching, timing, and status-tracking controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shixiangyu2](https://clawhub.ai/user/shixiangyu2)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, social media operators, and personal-brand builders use this skill to generate Xiaohongshu-style post drafts, organize them into a local publishing page, and manage copy, planned timing, and published status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can run unwanted browser code if crafted topic or brand text is used.

Mitigation: Use trusted topic and brand inputs, review generated pages before opening or sharing them, and fix HTML escaping before handling untrusted input.

Risk: Generated HTML, generated JSON files, and browser-side publication state can persist locally.

Mitigation: Store outputs only in intended locations, remove generated files when no longer needed, and clear local browser state for sensitive publishing workflows.

Risk: The artifact lists python>=3.8 in requirements.txt even though interpreter versions are not installable packages.

Mitigation: Remove python>=3.8 from requirements.txt and document the required Python interpreter version separately.

Risk: Demo and test scripts may create example files and can open a browser after user prompts.

Mitigation: Run demos and tests in a controlled workspace and review generated example files before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shixiangyu2/skills/xiaohongshu-hot-publish)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub](https://clawhub.ai)
- [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)
- [Semantic Versioning](https://semver.org/lang/zh-CN/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with Python and shell commands; generated artifacts are HTML and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated pages may persist publication state locally in the browser and create companion JSON data files.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence and artifact/CHANGELOG.md, released 2026-03-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
