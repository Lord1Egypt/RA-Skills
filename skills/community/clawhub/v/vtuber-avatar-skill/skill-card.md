## Description:

Generate VTuber avatar creator images via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate VTuber avatar image URLs from text prompts through the Neta AI image generation API, with optional size and reference-image controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image IDs, and the Neta API token are sent to api.talesofai.com.

Mitigation: Use a limited-scope token and avoid submitting sensitive prompts, personal data, or private reference images.

Risk: Passing real tokens directly on the command line can expose credentials through shell history or process inspection.

Mitigation: Prefer a secret manager or environment-based wrapper when operating the skill, and rotate tokens that may have been exposed.

Risk: The generated image URL and completion behavior depend on an external image-generation service.

Mitigation: Review generated outputs before use and handle service errors, moderation delays, or timeouts in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/vtuber-avatar-skill)
- [Neta AI API token page](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text URL with optional Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token and may use size and reference-image options.]

## Skill Version(s):

2.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
