## Description:

Turns stories, novels, and memoirs into a comic-creation workflow for publishable HTML comics with image panels, multi-panel layouts, dialogue and thought bubbles, narration, sound effects, watercolor style anchoring, and character consistency controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[piprot](https://clawhub.ai/user/piprot)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agents use this skill to convert user-provided stories, memoirs, or short fiction into scripted comic episodes, image-generation prompts, character/style references, HTML assembly, and compressed publishing outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled compression script can delete unrelated files if pointed at an existing destination folder.

Mitigation: Use the compression script only with a newly created, dedicated output folder such as comic_publish, and avoid project roots or documents folders.

Risk: Publishing generated HTML from untrusted story text can carry content injection risk.

Mitigation: Escape or sanitize story text before publishing generated HTML that includes untrusted input.

Risk: The default workflow and template are Chinese-language oriented and load Google Fonts.

Mitigation: Localize text and replace or self-host fonts when the deployment environment requires different language, privacy, or network behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/piprot/skills/story-comic-creator)
- [Skill workflow source](artifact/SKILL.md)
- [Comic script template](artifact/templates/script_template.md)
- [HTML comic template](artifact/templates/comic_template.html)
- [Compression script](artifact/templates/compress.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with templates, HTML/CSS, Python utility code, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents through staged comic scripting, image prompt creation, HTML assembly, and optional compression for publishing.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact frontmatter and manifest list 1.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
