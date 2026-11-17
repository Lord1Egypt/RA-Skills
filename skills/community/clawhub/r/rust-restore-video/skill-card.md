## Description:

Generates vertical WeryAI rust-restoration short videos from text briefs or rusty-object images, focusing on grind, polish, rust removal, and shine-reveal motion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to generate vertical rust-restoration short videos from text briefs or public HTTPS rusty-object images. The agent expands short prompts, confirms WeryAI parameters, invokes the bundled CLI, and returns playable video URLs or clear failure details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local image inputs can cause the helper script to read a local file and upload it to WeryAI file storage.

Mitigation: Prefer public HTTPS image URLs; allow local paths only after explicit user consent, and run the skill in a limited workspace or container with only intended files accessible.

Risk: Generation and status calls require WERYAI_API_KEY and successful runs consume WeryAI credits.

Mitigation: Keep the API key private and scoped, never commit it, and require confirmation before paid generation runs or retries.

Risk: Unsupported model parameters can cause API failures or unexpected results.

Mitigation: Validate model, duration, aspect ratio, audio, image, and optional fields against the bundled WeryAI reference and the skill's frozen model tables before submitting.

## Reference(s):

- [WeryAI video CLI and JSON reference](artifact/resources/WERYAI_VIDEO_API.md)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/rust-restore-video)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, json, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI payloads; final generation results are returned as text or JSON containing video URLs or error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, network access to WeryAI APIs, and user confirmation before paid generation runs.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
