## Description: <br>
Z.AI Vision analysis using GLM-4.6V model for image and video understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twolfe1991-cloud](https://clawhub.ai/user/twolfe1991-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to analyze images and short videos with the Z.AI Vision API, including OCR, screenshot diagnosis, UI design review, technical diagram interpretation, chart reading, and scene description. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, videos, and prompts are sent to Z.AI for processing. <br>
Mitigation: Use only approved visual inputs and avoid screenshots, recordings, documents, or diagrams containing secrets, personal data, regulated data, or confidential business information unless approved. <br>
Risk: The skill requires a sensitive Z.AI API key. <br>
Mitigation: Use a dedicated API key where possible, store it in the environment as ZAI_API_KEY, and avoid embedding it in prompts, files, or command history. <br>
Risk: The skill depends on the zai-sdk package at runtime. <br>
Mitigation: Pin or verify the zai-sdk dependency in controlled environments before deployment. <br>


## Reference(s): <br>
- [Z.AI Vision API Reference](references/API.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON analysis output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZAI_API_KEY; scripts support model, max token, temperature, and JSON output options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
