## Description:

YouTube analytics and research API guidance for searching channels, finding video outliers, retrieving video details, transcripts, and comments, and running TubeLab scans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antoniojps](https://clawhub.ai/user/antoniojps)

### License/Terms of Use:


## Use Case:

Developers, analysts, and creator-research teams use this skill to query TubeLab's YouTube research API for niche discovery, competitor analysis, channel analytics, outlier videos, transcripts, comments, and asynchronous scan workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a TubeLab API key.

Mitigation: Provide the key only to agents that should access the TubeLab account, and avoid exposing it in logs or shared outputs.

Risk: Some endpoints consume TubeLab credits, and POST /scan can spend 50-100 credits.

Mitigation: Confirm intent before starting scans or other paid API actions, and prefer cached or free endpoints where they satisfy the task.

Risk: Transcript and comment endpoints may return user-generated content.

Mitigation: Retrieve, store, and redistribute transcripts or comments only when needed for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antoniojps/skills/tubelab-api)
- [TubeLab API documentation](https://tubelab.net/docs/api/introduction)
- [TubeLab developers](https://tubelab.net/developers)
- [TubeLab pricing](https://tubelab.net/pricing)
- [YouTube Niche Finder](https://tubelab.net/youtube-niche-finder)
- [YouTube Outliers Finder](https://tubelab.net/youtube-outliers-finder)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, JSON]

**Output Format:** [Markdown reference material with curl commands, jq examples, endpoint tables, and JSON request/response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and TUBELAB_API_KEY; API responses are rate limited and some endpoints consume TubeLab credits.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
