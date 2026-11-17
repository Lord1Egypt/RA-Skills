## Description:

Analyze local image files with Ollama Cloud's Kimi K2.5 vision model to describe, understand, or answer questions about image content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kawummuwe-stack](https://clawhub.ai/user/kawummuwe-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to submit local images, screenshots, charts, diagrams, or memes to Ollama Cloud and receive natural-language descriptions or answers to targeted questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The selected image and prompt are sent to Ollama Cloud for analysis.

Mitigation: Use only images you have permission to upload, and avoid sensitive screenshots, private documents, regulated data, or other confidential content.

Risk: The helper requires an Ollama Cloud API key in the OLLAMA_API_KEY environment variable.

Mitigation: Configure the key only in trusted environments and avoid exposing it in shared shell history, logs, or screenshots.

## Reference(s):

- [Ollama API settings](https://ollama.com/settings)
- [Ollama generate API endpoint](https://ollama.com/api/generate)
- [ClawHub skill page](https://clawhub.ai/kawummuwe-stack/skills/vision-analyzer)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text from a command-line helper, with setup and usage guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OLLAMA_API_KEY and a user-selected JPG, PNG, GIF, or WebP image path.]

## Skill Version(s):

1.0.1 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
