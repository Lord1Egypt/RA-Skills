## Description: <br>
Generates short ASMR soap or wax cutting videos from a text prompt or a public HTTPS image, emphasizing clean slices, exposed cross-sections, falling powder, and cutting sound. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and agent users use this skill to prepare and run WeryAI video-generation requests for vertical soap or wax cutting ASMR clips. It supports text-to-video prompts and image-to-video generation from public HTTPS image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to WERYAI_API_KEY and sends generation requests to WeryAI. <br>
Mitigation: Install only when the user is comfortable granting the API key, and keep the key in the runtime environment rather than embedding it in prompts or files. <br>
Risk: Prompts and public HTTPS image URLs are transmitted to WeryAI and may include user-provided content. <br>
Mitigation: Review prompts and image URLs before confirming generation, and use only public image URLs that are appropriate to share with the provider. <br>
Risk: Generation requests may consume WeryAI provider credits. <br>
Mitigation: Confirm the model, duration, audio setting, and image URL before executing the CLI generation command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/soap-cut-video) <br>
- [Publisher profile](https://clawhub.ai/user/zoucdr) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with Node.js CLI commands; script stdout is JSON containing task status, error details, and generated video URLs when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and WERYAI_API_KEY. Requests send prompts and, for image workflows, public HTTPS image URLs to WeryAI.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
