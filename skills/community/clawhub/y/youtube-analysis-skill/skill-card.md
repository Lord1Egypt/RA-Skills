## Description:

Analyze YouTube videos with summary and deep-dive analysis. Use when a user provides a YouTube URL and wants both a summary and analytical insights about the content, implications, quality, and intersections with other topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sidonsoft](https://clawhub.ai/user/sidonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract YouTube transcripts when available, assess caption quality, and produce a grounded summary plus deeper analysis of claims, implications, credibility, and gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied YouTube URLs may be passed into a command execution path without enough validation.

Mitigation: Validate HTTPS YouTube URLs and pass command arguments without shell interpolation before transcript extraction.

Risk: Noisy or unavailable captions can lead to incomplete or misleading summaries.

Mitigation: Treat transcripts as source material rather than verified truth, lower confidence when captions are poor, and separate speaker claims from established facts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sidonsoft/skills/youtube-analysis-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with Summary and Analysis sections, supported by transcript extraction command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [States lower confidence when transcripts are missing, noisy, or based only on auto-captions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
