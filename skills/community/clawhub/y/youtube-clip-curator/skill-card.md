## Description:

Analyzes long-form YouTube videos, MP4 files, or transcripts to identify ranked short clip candidates with timestamps, titles, hooks, emotion tags, and optional editing assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noahcraft-open](https://clawhub.ai/user/noahcraft-open)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, editors, and agents use this skill to turn long YouTube videos, local MP4s, or transcripts into ranked clipping plans and optional editing deliverables. It is most useful when a user needs start and end timestamps, click-oriented titles, hook descriptions, emotion tags, and briefs for downstream editing or thumbnail work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media or transcript inputs may contain copyrighted, private, or confidential content.

Mitigation: Only provide media or transcripts you have rights to process, and avoid private or confidential recordings unless sharing them with the active agent and tools is acceptable.

Risk: Generated clip titles and tags may follow an unintended language or locale style.

Mitigation: Specify the desired language, locale, and style constraints before asking the agent to curate clips.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/noahcraft-open/skills/youtube-clip-curator)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Guidance]

**Output Format:** [Markdown or JSON, with optional FCPXML, DaVinci Resolve script, thumbnail brief JSON, and SRT subtitle content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranked clip candidates include start and end timestamps, scores, suggested titles, hook descriptions, expected appeal, emotion tags, peak frame timestamps, and reasoning.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
