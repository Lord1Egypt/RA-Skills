## Description:

Wuli Skill generates AI images and videos through the Wuli.art open platform API, including text-to-image, image editing, text-to-video, image-to-video, first-last-frame video, auto-video, uploads, and no-watermark downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sir1st-inc](https://clawhub.ai/user/sir1st-inc)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative teams use this skill to generate or edit images and videos from prompts and reference media through Wuli.art. It supports batch image generation, first-frame animation, first-last-frame video, and auto-video workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, API credentials, and optional reference media to Wuli.art and returned OSS upload URLs.

Mitigation: Use only non-sensitive prompts and media, prefer trusted source URLs, and run in a network-restricted environment when possible.

Risk: The optional WULI_EXTRA_COOKIE environment variable can add a Cookie header to API requests.

Mitigation: Leave WULI_EXTRA_COOKIE unset unless it is explicitly needed, and clear the variable after use.

Risk: Generated files may be saved into the current directory and opened automatically with the operating system viewer.

Mitigation: Run the skill from a controlled working directory and review downloaded files before sharing or reusing them.

## Reference(s):

- [Wuli Open Platform API Documentation](references/%E3%80%90%E5%91%9C%E5%93%A9Wuli%E3%80%91%E5%BC%80%E6%94%BE%E5%B9%B3%E5%8F%B0%20API%20%E6%96%87%E6%A1%A3.md)
- [Wuli.art](https://wuli.art)
- [Wuli Open Platform API](https://platform.wuli.art)
- [Wuli Skill on ClawHub](https://clawhub.ai/sir1st-inc/skills/wuli)
- [ClawHub publisher profile](https://clawhub.ai/user/sir1st-inc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; generated image or video files may be downloaded by the script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WULI_API_TOKEN. The script can upload local or remote reference media, submit and poll Wuli.art generation jobs, download generated media, and open downloaded files locally.]

## Skill Version(s):

1.0.9 (source: server release metadata, SKILL.md frontmatter, manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
