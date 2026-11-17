## Description:

Searches multiple online archives to find and recover deleted YouTube videos, metadata, and comments using a video ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upintheairsheep](https://clawhub.ai/user/upintheairsheep)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to check whether a deleted, missing, or private YouTube video has archived video, metadata, or comments and to report available archive links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube video IDs are sent to a named third-party archive lookup service.

Mitigation: Use the skill only when sharing the video ID with that service is acceptable.

Risk: Recovered links may point to deleted, private, copyrighted, paywalled, or incomplete archive material.

Mitigation: Use recovered links responsibly and preserve any service notes about access limits or availability.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upintheairsheep/skills/youtube-video-finder)
- [Find YouTube Video lookup API](https://findyoutubevideo.thetechrobo.ca/api/v5/{videoid})

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary of archive status, recovered links, services, and access notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recovered video, metadata, and comment links; raw/debug or JSONL details are only used when requested.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
