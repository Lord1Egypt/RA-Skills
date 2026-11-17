## Description:

Sum2Slides converts plain text or Markdown summaries into structured PowerPoint presentations with configurable templates, themes, and output settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to turn meeting notes, research summaries, project reports, and similar text into editable slide decks. It supports local command-line or Python API use with configurable presentation templates and themes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic chat or keyword triggering can process private or irrelevant messages into slide decks.

Mitigation: Keep the skill limited to explicit commands where possible, and disable or tightly scope automatic keyword triggering for private chats.

Risk: Generated slides may contain incorrect summaries or sensitive content before sharing.

Mitigation: Review generated presentations before distribution and avoid using private or confidential input unless the deployment policy allows it.

Risk: The artifact includes examples that reference a hardcoded Feishu owner_open_id.

Mitigation: Replace any Feishu owner_open_id with the deployment owner's own ID before use.

Risk: Dependency installation may pull packages from untrusted sources.

Mitigation: Install dependencies in a virtual environment from trusted package indexes and review dependency versions before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wwumit/skills/sum2slides)
- [Skill Documentation](artifact/SKILL.md)
- [Package README](artifact/README.md)
- [OpenClaw Usage Guide](artifact/OPENCLAW_USAGE_GUIDE.md)
- [Release Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance and generated PowerPoint (.pptx) files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text or Markdown input, output path selection, templates, themes, slide limits, and font settings.]

## Skill Version(s):

1.0.1 (source: server release metadata, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
