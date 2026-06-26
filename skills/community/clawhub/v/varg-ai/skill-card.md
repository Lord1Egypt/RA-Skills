## Description: <br>
Generate AI videos, images, speech, and music using Varg for videos, animations, talking characters, slideshows, product showcases, social content, or single-asset generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[securityqq](https://clawhub.ai/user/securityqq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and external users use this skill to generate media assets and compose rendered videos through Varg cloud or local rendering workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential exposure involving VARG_API_KEY or BYOK provider keys. <br>
Mitigation: Use a dedicated low-balance Varg key, keep raw secrets out of prompts and logs, and reference credentials through environment variables. <br>
Risk: Unpinned update behavior can change skill instructions before use. <br>
Mitigation: Avoid automatic updates unless the updated skill files are re-reviewed and rescanned. <br>
Risk: Paid renders or credit purchases can create unexpected costs. <br>
Mitigation: Confirm every paid render and credit package with the user before submitting requests. <br>
Risk: Media prompts, uploaded files, generated outputs, or project content may be sent to remote Varg services and cached. <br>
Mitigation: Do not upload private photos, confidential code, or sensitive media unless remote processing and public URLs are acceptable. <br>


## Reference(s): <br>
- [Varg homepage](https://varg.ai) <br>
- [ClawHub skill page](https://clawhub.ai/securityqq/varg-ai) <br>
- [Cloud Render Mode](references/cloud-render.md) <br>
- [Local Render Mode](references/local-render.md) <br>
- [Gateway API Reference](references/gateway-api.md) <br>
- [Models](references/models.md) <br>
- [Bring Your Own Key](references/byok.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, curl, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VARG_API_KEY; may use curl for cloud rendering or bun and ffmpeg for local rendering; media generation can consume paid credits.] <br>

## Skill Version(s): <br>
2.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
