## Description:

Researches a YouTube topic with the official YouTube Data API v3 - top videos, view and engagement statistics, titles, tags and gaps - and writes research.md for a video project. Use when the user wants topic ideas, competitor or trend research, or evidence for a YouTube video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and video producers use this skill to research YouTube topics, compare popular videos and engagement, identify content gaps, and plan original video angles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Google and API requests consume quota.

Mitigation: Agree on 1–3 queries before searching, restrict the API key to YouTube Data API v3, and stop when quota is exhausted.

Risk: Research could present unsupported or misleading video statistics or claims.

Mitigation: Use only statistics returned by the script and cite video URLs for report claims.

## Reference(s):

- [YouTube setup instructions](references/setup.md)
- [YouTube Data API quota costs](https://developers.google.com/youtube/v3/determine_quota_cost)

## Skill Output:

**Output Type(s):** [Analysis, Files]

**Output Format:** [Markdown research report (research.md) with cited video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a top-video table, topic patterns, content gaps, and 3–5 proposed original video angles.]

## Skill Version(s):

0.3.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
