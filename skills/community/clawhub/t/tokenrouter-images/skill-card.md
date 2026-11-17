## Description:

Generate or edit images through Palebluedot Ai(PBD)-TokenRouter's multimodal image generation endpoint (`/v1/chat/completions`) using TokenRouter-compatible image models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yb98k999](https://clawhub.ai/user/yb98k999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate new images or edit existing images through TokenRouter-supported image models, including model overrides and provider image configuration options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected input images are sent to TokenRouter for image generation or editing.

Mitigation: Install and use the skill only when this third-party processing is acceptable for the data being submitted.

Risk: API-key handling is security-sensitive, and the evidence security summary flags the documented key handling as risky.

Mitigation: Use a session-scoped environment variable or protected secret store, avoid placing keys in chat or shell history, and prefer revocable limited keys when available.

## Reference(s):

- [TokenRouter docs](https://www.tokenrouter.com/docs)
- [TokenRouter](https://www.tokenrouter.com)
- [ClawHub skill page](https://clawhub.ai/yb98k999/skills/tokenrouter-images)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash command examples; script output is a saved image file path and status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TokenRouter API key and writes generated or edited images to the requested output path.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
