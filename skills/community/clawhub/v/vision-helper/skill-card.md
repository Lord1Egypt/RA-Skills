## Description: <br>
Analyze images using local or cloud vision models via Ollama to identify content, inspect UI screenshots, and extract text with OCR support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ravenquasar](https://clawhub.ai/user/ravenquasar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to analyze screenshots, UI captures, and other images for visual description, OCR, and interface understanding through a configured Ollama vision endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots and images may contain passwords, confidential data, or other sensitive content that is sent to the configured Ollama or cloud vision endpoint. <br>
Mitigation: Keep OLLAMA_API_URL on localhost for private images, avoid analyzing sensitive screenshots, and use cloud models only when the image is safe to share with that provider. <br>
Risk: The helper reads image files from paths supplied by the user, including readable directories outside the current workspace. <br>
Mitigation: Provide only intended image paths, avoid broad automation over unreviewed directories, and rely on the built-in file type and size validation before sending images for analysis. <br>
Risk: Vision model output can be incomplete or incorrect, especially when used to drive browser, desktop, or game automation decisions. <br>
Mitigation: Review the returned analysis before taking consequential actions and add task-specific checks when using the skill in automated workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ravenquasar/vision-helper) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text analysis from the configured vision model, with shell command examples for invoking the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts an image path, optional prompt, optional model name, and environment-configured timeout and Ollama API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
