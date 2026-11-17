## Description:

Studio-grade AI image and video generation for photorealistic portraits, product shots, stickers, animations, and more from natural-language prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[montenegronyc](https://clawhub.ai/user/montenegronyc)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate or transform images, video, and audio through Perstudio from natural-language prompts and optional uploaded media. It also supports setup guidance, balance checks, and configuration of the required API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to globally install a mutable third-party npm plugin that was not included for review.

Mitigation: Review the npm package and publisher before installing, and prefer a pinned version or isolated install when possible.

Risk: The skill requires a Perstudio API key for cost-bearing generation requests.

Mitigation: Configure the API key with least necessary access, keep it out of prompts and logs, and monitor balance before running large generation batches.

Risk: Uploaded local files are sent to perstudio.ai.

Mitigation: Upload only files intended for Perstudio processing and verify paths before calling upload_asset.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/montenegronyc/skills/skill-perstudio)
- [Perstudio service homepage](https://perstudio.ai)
- [Perstudio pricing](https://perstudio.ai/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline tool-call examples and configuration commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PERSTUDIO_API_KEY. Media generation consumes Perstudio tokens, and uploaded files should be limited to files the user intends to send to perstudio.ai.]

## Skill Version(s):

3.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
