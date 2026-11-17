## Description:

Analyze images using local or cloud vision models via Ollama to identify content, UI elements, screenshots, or extract text with OCR support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ravenquasar](https://clawhub.ai/user/ravenquasar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to analyze local images or screenshots, inspect UI content, and perform OCR with an Ollama vision model when longer model timeouts are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local images and screenshots from broad filesystem locations, which may expose credentials, private documents, or sensitive desktop content.

Mitigation: Use it only on images intended for analysis, prefer workspace or temporary paths, and avoid screenshots containing secrets or private documents.

Risk: Image data can be sent to a configurable Ollama endpoint, including cloud or remote models.

Mitigation: Keep OLLAMA_API_URL on localhost for routine use, and configure a remote endpoint only when that service is explicitly trusted for the image contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ravenquasar/skills/vision-helper)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text image analysis from the configured vision model; usage guidance includes shell commands and environment variables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts an image path, optional prompt, optional model name, and environment configuration for model, timeout, and Ollama API URL.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
