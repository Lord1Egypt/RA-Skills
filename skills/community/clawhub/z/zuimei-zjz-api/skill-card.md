## Description: <br>
AI photo-processing API integration for ID photo creation, portrait segmentation, face enhancement, background replacement, layout, and image editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flaravel](https://clawhub.ai/user/flaravel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare ID-style photos, remove or replace portrait backgrounds, enhance face photos, generate printable layouts, and adjust image size or format through the Zuimei photo-processing API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send sensitive face or ID photos to a third-party photo-processing API without clear consent, retention, or cleanup controls. <br>
Mitigation: Ask for explicit user consent before uploading images, avoid highly sensitive identity documents unless the provider's privacy terms are understood, and delete local uploads or results when no longer needed. <br>
Risk: The artifact embeds shared test API credentials. <br>
Mitigation: Use scoped user-owned credentials from environment variables or a secret manager, remove shared credentials from release artifacts, and rotate any exposed keys. <br>
Risk: Broad photo-processing triggers can cause unintended use for user images. <br>
Mitigation: Confirm the requested operation and destination service before processing images, especially for ID-photo, portrait, or face-enhancement workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/flaravel/zuimei-zjz-api) <br>
- [Zuimei Website](https://zuimei.huipai.vip) <br>
- [API Documentation](artifact/API.md) <br>
- [OpenAPI Specification](artifact/openapi.yaml) <br>
- [Usage Examples](artifact/examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline Python and shell command snippets, JSON API responses, and result image URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user photos and API credentials; successful API calls can return hosted image result URLs.] <br>

## Skill Version(s): <br>
0.1.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
