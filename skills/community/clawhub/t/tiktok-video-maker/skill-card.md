## Description:

Generate TikTok-style talking videos from a script and image using the LovelyBots API, including job submission, polling for completion, and retrieval of a download URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georgegally](https://clawhub.ai/user/georgegally)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketing teams, ecommerce brands, and developers use this skill to generate short talking videos from scripts and source images through the LovelyBots API. It is suited for agent workflows that need to queue video generation, monitor status, and return a finished video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-submitted scripts and images are sent to LovelyBots for video generation.

Mitigation: Use the skill only with content the user is comfortable uploading to LovelyBots, and avoid sending sensitive personal or proprietary media unless the deployment has approved handling controls.

Risk: The documented API can make generated videos public unless private generation is requested.

Mitigation: Set public generation to false by default and get explicit user intent before creating public videos.

Risk: Share URLs may allow unintended access to generated videos if logged or shared broadly.

Mitigation: Treat share URLs as sensitive links, return them only when useful to the user, and avoid storing them in broad logs or public channels.

Risk: The skill relies on a bearer API token for LovelyBots requests.

Mitigation: Store LOVELYBOTS_API_KEY as a secret, avoid committing it to files, and rotate or revoke the token if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georgegally/skills/tiktok-video-maker)
- [LovelyBots OpenClaw documentation](https://lovelybots.com/openclaw)
- [LovelyBots developer API keys](https://lovelybots.com/developer)
- [LovelyBots API base URL](https://api.lovelybots.com/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, shell command examples, and final video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a LovelyBots API key, curl, python3 for the polling example, and public http/https URLs when image input is provided by URL.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
