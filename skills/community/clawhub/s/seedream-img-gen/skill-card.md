## Description: <br>
Generates images with ByteDance Seedream models on Volcengine Ark, supporting text-to-image and image-to-image workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anpupil](https://clawhub.ai/user/anpupil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure Volcengine Ark credentials, choose Seedream models, and generate image assets from prompts or reference images through SDK, OpenAI-compatible, or command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup guidance can expose the Volcengine Ark API key if the key is printed to logs, terminals, or shared transcripts. <br>
Mitigation: Check for credential presence without printing secret values, keep API keys private, and avoid storing them in command history or generated artifacts. <br>
Risk: Running the generator can consume paid Volcengine quota and download generated content to local files. <br>
Mitigation: Confirm model choice, prompt, image count, output path, and billing expectations before execution. <br>
Risk: The script depends on external Python packages and a remote image-generation API. <br>
Mitigation: Install dependencies from trusted sources in an isolated environment and review network/API use before running. <br>


## Reference(s): <br>
- [Seedream API Reference](artifact/references/api_reference.md) <br>
- [Volcengine Ark Documentation](https://www.volcengine.com/docs/82379) <br>
- [Volcengine Ark Console](https://console.volcengine.com/ark) <br>
- [ClawHub Release Page](https://clawhub.ai/anpupil/seedream-img-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell and Python examples; generated image files when the bundled script is executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Volcengine Ark API key and Python dependencies; generated images may be saved from URL or base64 responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
