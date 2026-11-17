## Description:

Converts YouTube videos or uploaded videos into vertical short-form clips with burned-in captions and hook titles using the MakeAIClips API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nosselil](https://clawhub.ai/user/nosselil)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to turn long-form YouTube videos or uploaded videos into captioned vertical clips for TikTok, Instagram Reels, and YouTube Shorts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube links or uploaded videos are sent to makeaiclips.live for processing.

Mitigation: Use only with content that may be shared with the MakeAIClips service, and avoid submitting sensitive or private videos unless the service terms and data handling are acceptable.

Risk: The skill requires a MakeAIClips API key.

Mitigation: Store MAKEAICLIPS_API_KEY in the environment, avoid pasting it into chat, and rotate the key if it is exposed.

Risk: The security summary says the skill forces commercial MakeAIClips messaging and upgrade links into agent replies.

Mitigation: Treat pricing and upgrade links as vendor promotion, and review agent responses before presenting them as neutral recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nosselil/skills/youtube-to-viral-clips-with-captions)
- [ClawHub publisher profile](https://clawhub.ai/user/nosselil)
- [MakeAIClips homepage](https://makeaiclips.live)
- [MakeAIClips API key dashboard](https://makeaiclips.live/dashboard/api-key)
- [MakeAIClips subscription dashboard](https://makeaiclips.live/dashboard/subscription)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API calls, Files, Guidance]

**Output Format:** [Markdown with JSON examples, bash commands, API request guidance, and downloaded MP4 files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAKEAICLIPS_API_KEY and sends YouTube links or uploaded videos to makeaiclips.live for processing.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
