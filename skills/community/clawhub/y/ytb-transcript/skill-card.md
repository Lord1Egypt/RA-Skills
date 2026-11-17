## Description:

Fetches YouTube video transcripts, subtitles, timestamped text, and AI-generated summaries from a video URL or ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rqcker](https://clawhub.ai/user/rqcker)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, students, and developers use this skill to extract YouTube subtitles or transcripts and turn long-form video content into summaries, notes, and key points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Referenced helper files are not bundled, so runtime transcript fetching behavior may vary or be unavailable.

Mitigation: Confirm the installed package includes the expected helper files or have the agent explain how it will fetch transcripts before relying on the result.

Risk: Multilingual videos may return subtitles in an unintended language.

Mitigation: Ask the user for the preferred subtitle language when language matters.

Risk: Generated summaries can omit context or reflect errors in available subtitles.

Mitigation: Review the returned transcript or timestamps before using summaries for decisions, citations, or study notes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rqcker/skills/ytb-transcript)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown transcript, subtitles, timestamps, summaries, and key points]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May vary by available subtitles, selected language, video length, and summary detail requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
