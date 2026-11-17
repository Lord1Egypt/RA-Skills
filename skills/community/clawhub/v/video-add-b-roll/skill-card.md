## Description:

Adds deliberate, transcript-timed visual cutaways from local footage or Pexels to talking-head, interview, documentary, and explanatory videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whitetowerai](https://clawhub.ai/user/whitetowerai)

### License/Terms of Use:

MIT-0

## Use Case:

Video editors and production agents use this skill to select, review, and add relevant B-roll to an existing transcript-aligned video project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running media tools against the wrong project can modify local video files or create unwanted review artifacts.

Mitigation: Confirm the intended project root and review generated pages and receipts before applying changes.

Risk: Stock-media access uses a Pexels API key and contacts Pexels.

Mitigation: Keep the key in the local environment or .env file; do not share it in chat, commands, or review artifacts.

Risk: An irrelevant or misleading cutaway can misrepresent the spoken content.

Mitigation: Review candidate relevance, provenance, and final video before approving delivery; skip shots without suitable footage.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/whitetowerai/skills/video-add-b-roll)
- [B-Roll Rules](reference/broll-rules.md)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Markdown, Shell commands, Video files]

**Output Format:** [Markdown guidance, JSON plans and review records, and video deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final delivery requires review and verification of selected footage.]

## Skill Version(s):

1.0.4 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
