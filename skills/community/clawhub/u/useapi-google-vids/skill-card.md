## Description:

Make Gemini Omni 1.2 Flash videos and talking AI avatars in Google Vids through the third-party useapi.net API, using the user's connected Google account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[useapi](https://clawhub.ai/user/useapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate and refine short Google Vids clips, images, and talking avatar videos from prompts, reference media, or scripts through a connected useapi.net account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the useapi.net token to the third-party API and may upload local reference media.

Mitigation: Use the service only if you trust it, keep the token in USEAPI_TOKEN, and submit only media you are authorized to share.

Risk: Video, image, and avatar generation uses account allowances, and some unclear failures may still consume usage.

Mitigation: Review the requested generation and available allowance first; do not blindly resend an unclear failed request, and download results promptly because remote files expire.

## Reference(s):

- [Google Vids API documentation](https://useapi.net/docs/api-google-vids-v1?utm_source=clawhub.ai&utm_medium=skill&utm_campaign=clawhub-google-vids)
- [Set up a useapi.net account](https://useapi.net/docs/start-here/setup-useapi)
- [Connect Google Vids](https://useapi.net/docs/start-here/setup-google-vids)
- [useapi.net subscription](https://useapi.net/docs/subscription)
- [ClawHub skill release](https://clawhub.ai/useapi/skills/useapi-google-vids)

## Skill Output:

**Output Type(s):** [Files, Text, JSON]

**Output Format:** [MP4 video, JPEG image, JSON job records, and text status and saved-file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated clips are typically 3 to 15 seconds; extensions can reach about 34 seconds. Avatar videos can be up to 30 seconds. Media is saved locally; generated video and image links have limited availability.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
