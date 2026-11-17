## Description:

Seedream5 helps agents call the Seedream5.0 image generation API for text-to-image and reference-image generation with prompt, size, watermark, and image URL parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runninghcm](https://clawhub.ai/user/runninghcm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate images, posters, covers, and reference-image variations through the Seedream5.0 API while preserving prompt, size, watermark, and image parameter validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved API key files may be loaded by helper scripts during generation.

Mitigation: Prefer a session-scoped X_API_KEY, avoid saving keys with set_key.sh unless reviewed, and verify any local .env file before running generate.sh.

## Reference(s):

- [Seedream5.0 API Guide](references/api-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/runninghcm/skills/seedream5-official)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text summaries with optional shell command output and API response excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated image URLs and defaulted parameter summaries; does not return OCR, video, or non-generative image edits.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
