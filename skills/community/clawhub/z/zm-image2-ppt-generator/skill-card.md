## Description:

ZM Image2PPT 视觉幻灯片生成。用于根据 Markdown 大纲或 slides_plan.json 生成视觉化幻灯片图片、HTML viewer 和 16:9 PPTX；正式项目需配合 ZM PPT/Deck 正式生产流程使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and presentation authors use this skill to turn a Markdown outline or slides_plan.json into visual slide images, an HTML viewer, and a 16:9 PPTX deck. It supports built-in visual styles and optional template cloning for project slide production workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marks the release suspicious because optional automation and configuration paths should be reviewed before installation.

Mitigation: Install only if you trust the publisher, review the skill before deployment, and use an isolated virtual environment for Python dependencies.

Risk: Configured image or vision providers may receive slide content, template images, or related prompts.

Mitigation: Use trusted providers and relay endpoints only, and avoid using proprietary templates with untrusted relay endpoints.

Risk: The optional codex backend adds an automation path that is not recommended for untrusted slide content.

Mitigation: Prefer the maintained scripts/generate_ppt.py path and avoid --backend codex for untrusted slide content.

Risk: The skill writes generated outputs and caches under the caller's working directory.

Mitigation: Run it in an appropriate project directory and review generated outputs, template renders, and caches before sharing or committing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/zm-image2-ppt-generator)
- [OpenAI Images API guide](https://platform.openai.com/docs/guides/images)
- [English README](docs/README.en.md)
- [Installation guide](docs/install.md)
- [AI readiness checklist](checklists/ai_readiness_checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated slide assets such as PNG images, HTML viewer files, JSON prompts, and PPTX decks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts are written under the caller's working directory, commonly outputs/<timestamp>/, with template render and analysis caches when template cloning is used.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
