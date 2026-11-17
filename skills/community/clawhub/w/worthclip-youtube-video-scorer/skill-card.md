## Description:

Scores YouTube videos from 1 to 10 against a user's learning goals and persona, with feed, summary, alignment, and usage helpers backed by the WorthClip API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivanstancich](https://clawhub.ai/user/ivanstancich)

### License/Terms of Use:

MIT

## Use Case:

Learners, researchers, and agents use this skill to score YouTube videos for relevance, review a personalized scored feed, and inspect WorthClip API usage. It is useful when a user wants concise scoring and summary output aligned to their goals and persona.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends YouTube video IDs plus authenticated feed and usage requests to WorthClip's hosted Convex backend.

Mitigation: Use it only when the user intends to use WorthClip's hosted service and is comfortable sharing those request details with WorthClip.

Risk: The skill requires a WorthClip API key in WORTHCLIP_API_KEY.

Mitigation: Verify the WorthClip developer page before configuring the key, keep the key out of prompts and logs, and rotate it if exposure is suspected.

## Reference(s):

- [WorthClip](https://worthclip.com)
- [WorthClip Developers](https://worthclip.com/developers)
- [ClawHub Skill Page](https://clawhub.ai/ivanstancich/skills/worthclip-youtube-video-scorer)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl and jq with WORTHCLIP_API_KEY to call WorthClip API endpoints.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
