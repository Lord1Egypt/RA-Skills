## Description:

Generate, edit, and compose images using Gemini models from text prompts and input images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyan](https://clawhub.ai/user/wangyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to generate new images, edit photos, compose multiple images, and create assets such as logos, posters, icons, banners, covers, and brand visuals through Gemini-compatible image APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unverified installer commands may execute code from remote endpoints during setup.

Mitigation: Review installation commands before use and prefer trusted package-manager or ClawHub installation paths over curl-to-shell setup.

Risk: Shared .env loading can expose unrelated secrets to this skill at runtime.

Mitigation: Use a dedicated Gemini API key and prefer explicit command-line or skill-local configuration instead of broad shared .env files.

Risk: Custom base URLs receive prompts, input images, and API credentials.

Mitigation: Configure only trusted Gemini-compatible endpoints and avoid sending sensitive prompts or images to untrusted providers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyan/skills/wangyan-gemini-image-gen)
- [Publisher profile](https://clawhub.ai/user/wangyan)
- [Project homepage](https://github.com/wangyan/wangyan-skills)
- [Release changelog](https://github.com/wangyan/wangyan-skills/blob/main/CHANGELOG.md)
- [API formats reference](references/api-formats.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Saved image files with IMAGE_PATH status output and Markdown-oriented usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Gemini API key, trusted base URL, python3, uv, and messaging permission when the agent sends generated images to a user.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
