## Description:

Turns PDF technical reports into platform-specific promotional drafts for X threads, Xiaohongshu posts, WeChat articles, and optional image prompts or generated images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christianashannon](https://clawhub.ai/user/christianashannon)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, researchers, and developer relations teams use this skill to convert a PDF technical report into audience-specific launch and promotional content for X, Xiaohongshu, and WeChat. It can also prepare image specifications and optionally call image-generation providers when API credentials are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic package installation can change the execution environment during skill use.

Mitigation: Install reviewed, pinned dependencies in an isolated environment before running the skill.

Risk: Network-enabled image generation can send report-derived prompts to third-party providers.

Mitigation: Use --no-image for confidential reports or only configure image API credentials when external sharing is acceptable.

Risk: Broad network shell access can allow external requests during skill execution.

Mitigation: Run the skill with network controls appropriate to the report sensitivity and review any external API use before enabling credentials.

Risk: Processing untrusted PDF paths may expose the agent runtime to malformed or unexpected inputs.

Mitigation: Run the skill only on trusted PDFs in a constrained workspace and review extracted content before reuse.

## Reference(s):

- [Skill page](https://clawhub.ai/christianashannon/skills/tech-write-assist)
- [Image Prompt Engineering Guide](references/image-prompt-guide.md)
- [Platform Content Specifications](references/platform-specs.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown files with optional JSON image specifications and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces per-platform drafts, an image_specs.json file, optional generated images, and a summary report under an output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
