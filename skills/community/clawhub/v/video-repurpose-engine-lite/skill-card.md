## Description:

Pick the best short-clip timestamps from a video transcript (SRT/VTT or plain text with timestamps) — scores segments by hook potential and returns ranked clip windows. Local text analysis, no ffmpeg. Use when the user wants clip ideas from a podcast/video transcript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, podcasters, and editors use the skill to find promising short-clip windows in a supplied transcript and review the ranked timestamps and hook explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was incomplete: only 2 of 4 components were fully scanned, and the JavaScript files were only partially inspected.

Mitigation: Consider this coverage gap before installing and review the skill and its source before use.

Risk: Heuristic clip rankings can select weak or misleading excerpts.

Mitigation: Review each suggested window against the transcript and surrounding context before using it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/nenadzivotic/skills/video-repurpose-engine-lite)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON]

**Output Format:** [Ranked clip windows with timestamps, hook rationale, and transcript excerpts; the script report is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses heuristic scores and typically suggests 20–60 second windows; review the picks with judgment.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
