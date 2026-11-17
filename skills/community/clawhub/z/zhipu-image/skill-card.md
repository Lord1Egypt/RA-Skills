## Description:

Generates and downloads images through the Zhipu GLM-Image web experience by checking browser login state, capturing Zhipu cookies, calling the image.z.ai web endpoint, and saving results locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangm199](https://clawhub.ai/user/huangm199)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and image-generation users use this skill to prepare a Zhipu web login session, submit GLM-Image prompts, and download generated image files into a local captures directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to a Chrome remote-debugging browser and extracts Zhipu-related cookies.

Mitigation: Use a dedicated browser profile for Zhipu activity and run the skill only when you intentionally want it to access that profile.

Risk: The captured session is stored locally in plaintext.

Mitigation: Delete the local session JSON after use and avoid sharing the workstation or workspace with untrusted users.

Risk: The network monitor can print request details and POST bodies during debugging.

Mitigation: Run the monitor only for deliberate troubleshooting and avoid using it with sensitive prompts or unrelated logged-in browser activity.

## Reference(s):

- [Zhipu Image web app](https://image.z.ai/)
- [Zhipu Image API proxy endpoint](https://image.z.ai/api/proxy)
- [ClawHub skill page](https://clawhub.ai/huangm199/skills/zhipu-image)
- [ClawHub publisher profile](https://clawhub.ai/user/huangm199)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output; generated images are saved as local PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Chrome remote-debugging browser session on port 18800 and an authenticated Zhipu web session.]

## Skill Version(s):

2.0.0 (source: evidence.json release.version and artifact/scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
