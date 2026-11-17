## Description:

Wx Peitu generates PNG/JPEG illustration packs for WeChat long-form Markdown articles and can sync the results to Lark/Feishu Drive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, content marketers, and agent users use this skill to turn Markdown WeChat articles into a planned set of cover, body, data, flow, and back-cover illustrations ready for publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown-derived search terms or generated image material may be sent to third-party photo services.

Mitigation: Use non-sensitive articles, or disable external photo search when drafts or source material should stay private.

Risk: Generated files may be written to the desktop and uploaded to Lark/Feishu Drive automatically.

Mitigation: Disable or remove the cloud-sync and file-opening steps unless the user explicitly wants those side effects.

Risk: Zero-confirmation Master Mode can combine file access, network calls, and uploads without enough runtime control.

Mitigation: Use the confirmation-based workflow for sensitive drafts and review the illustration plan before generation.

Risk: The Puppeteer screenshot flow uses browser rendering settings and external assets that need hardening for untrusted Markdown.

Mitigation: Use a reviewed, pinned release and harden the screenshot script before processing untrusted Markdown or remote assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardwason/skills/wx-peitu)
- [Workflow reference](references/workflow.md)
- [Design system reference](references/design-system.md)
- [Quality gates reference](references/quality-gates.md)
- [Assets reference](references/assets.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, standalone HTML/CSS files, Puppeteer screenshot commands, and PNG/JPEG image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typical delivery includes a local desktop folder of generated images and optional Lark/Feishu Drive upload links; screenshot generation depends on Puppeteer-core and local Chrome or Chromium.]

## Skill Version(s):

7.4.0 (source: frontmatter, release evidence, changelog released 2026-07-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
