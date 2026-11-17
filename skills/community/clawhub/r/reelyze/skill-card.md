## Description:

Reelyze is an AI analyst for short-form video that can analyze public Instagram Reels, TikToks, and YouTube Shorts, transcribe videos, provide temporary MP4 or MP3 links, and generate scripts or content ideas through the Reelyze API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usamalatif](https://clawhub.ai/user/usamalatif)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media managers, brands, and agents use this skill to evaluate public short-form videos, summarize retention and hook feedback, retrieve transcripts or temporary media links, and draft scripts or content ideas from a topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends public video URLs, topics, and generated requests to the Reelyze API.

Mitigation: Use the skill only when the user is comfortable sharing those inputs with Reelyze, and avoid submitting private or non-public video URLs.

Risk: The skill requires a Reelyze API key for authenticated API calls.

Mitigation: Store REELYZE_API_KEY in the environment, avoid pasting it into shared chats or logs, and treat invalid or revoked credentials as a setup issue.

Risk: Changing REELYZE_BASE_URL can send requests and credentials away from the official Reelyze API endpoint.

Mitigation: Leave REELYZE_BASE_URL unset or set to https://api.getreelyze.com unless intentionally using a trusted Reelyze-controlled endpoint.

Risk: Download and audio URLs returned by the API are temporary.

Mitigation: Fetch or provide returned media links promptly and avoid presenting them as durable storage locations.

## Reference(s):

- [Reelyze homepage](https://getreelyze.com)
- [Reelyze API base URL](https://api.getreelyze.com)
- [ClawHub skill page](https://clawhub.ai/usamalatif/skills/reelyze)
- [Publisher profile](https://clawhub.ai/user/usamalatif)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown summaries, plain text transcripts, generated script structures, content idea lists, and curl-style API command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include temporary MP4 or MP3 URLs returned by the Reelyze API; full analysis and content generation can require paid plan credits.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
