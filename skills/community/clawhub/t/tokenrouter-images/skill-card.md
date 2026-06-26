## Description: <br>
Generate or edit images through Palebluedot Ai(PBD)-TokenRouter's multimodal image generation endpoint (`/v1/chat/completions`) using TokenRouter-compatible image models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yb98k999](https://clawhub.ai/user/yb98k999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate new images or edit existing images with TokenRouter-compatible image models, including model overrides and provider-specific image configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TokenRouter API keys may be exposed if pasted into chat or stored insecurely. <br>
Mitigation: Prefer a local environment variable or secret manager for PBD_TOKENROUTER_API_KEY and avoid sharing keys in conversation. <br>
Risk: Prompts and input images are sent to TokenRouter for generation or editing. <br>
Mitigation: Avoid sensitive prompts or private images unless the user is comfortable sending them to TokenRouter. <br>


## Reference(s): <br>
- [TokenRouter documentation](https://www.tokenrouter.com/docs) <br>
- [ClawHub skill page](https://clawhub.ai/yb98k999/tokenrouter-images) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; the script writes image files and prints the saved path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TokenRouter API key and may send prompts or input images to TokenRouter.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
