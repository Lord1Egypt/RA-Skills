## Description: <br>
Generates text-to-image outputs with the Doubao Seedream model, supports concurrent batch generation, and creates a local gallery preview page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aowind](https://clawhub.ai/user/aowind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn text prompts into one or more Doubao Seedream images, save JPEG outputs, record prompt mappings, and open a generated gallery preview. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts are sent to Doubao/Volcengine and may expose sensitive prompt content. <br>
Mitigation: Avoid secrets and sensitive personal data in prompts before running the skill. <br>
Risk: Batch generation can incur API costs, especially with higher count and worker settings. <br>
Mitigation: Review count, workers, model, and dry-run settings before making API calls. <br>
Risk: API keys can be exposed if pasted into chat or command history. <br>
Mitigation: Prefer ARK_API_KEY environment variables or a local ~/.doubao-image-gen/.env file over sharing keys in chat. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aowind/sjht-doubao-image-gen) <br>
- [Volcengine ARK console](https://console.volcengine.com/ark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces JPEG images, prompts.json mappings, index.html gallery previews, and GENERATED_IMAGE path lines.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and changelog, released 2026-03-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
