## Description: <br>
Generate images and text using Vultr Inference API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happytreees](https://clawhub.ai/user/happytreees) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Vultr's hosted inference service for image generation, text completions, model listing, and related setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and chat messages are sent to Vultr's hosted inference service. <br>
Mitigation: Avoid sending secrets, regulated data, or confidential content unless Vultr's data handling is acceptable for the intended use case. <br>
Risk: The skill requires a Vultr API key stored at ~/.config/vultr/api_key. <br>
Mitigation: Protect the API key file with appropriate local permissions and rotate the key if it may have been exposed. <br>
Risk: Generated images can be saved to local files using user-selected output paths. <br>
Mitigation: Choose output filenames deliberately and review files before sharing or overwriting existing assets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/happytreees/vultr-inference) <br>
- [Vultr Inference API models endpoint](https://api.vultrinference.com/v1/models) <br>
- [Vultr Inference image generation endpoint](https://api.vultrinference.com/v1/images/generations) <br>
- [Vultr Inference chat completions endpoint](https://api.vultrinference.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, Python examples, JSON API payloads, and optional generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Vultr API key file and can write generated images to caller-selected local filenames.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
