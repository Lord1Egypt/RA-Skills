## Description:

Analyzes short-form video ad transcripts and performance data to produce creator coaching feedback for improving pacing, word count, openings, and ROI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnshenopeninterx](https://clawhub.ai/user/shawnshenopeninterx)

### License/Terms of Use:


## Use Case:

Marketing teams, creator managers, and agents use this skill to analyze social video URLs or Excel performance data and draft concise creator feedback. It is best treated as lightweight transcript and ROI coaching rather than full visual ad analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video URLs are sent to Memories.ai for transcription, and the security guidance flags third-party processing as a review point.

Mitigation: Use only video URLs that are approved for Memories.ai processing; avoid unpublished, client-confidential, or highly sensitive campaign URLs unless that processing is acceptable.

Risk: The security summary says the real behavior is narrower than advertised and should be treated as lightweight transcript and ROI coaching.

Mitigation: Review generated advice before sharing it with creators and avoid relying on it as complete visual ad analysis.

Risk: The artifact depends on Python packages such as fpdf2, pandas, and openpyxl for report generation.

Mitigation: Install dependencies in an isolated environment with pinned versions where possible.

## Reference(s):

- [Creator Video Feedback Framework](references/creator-feedback-framework.md)
- [Memories.ai API Tools](https://api-tools.memories.ai)
- [Memories.ai Privacy Policy](https://memories.ai/privacy)
- [ClawHub Skill Page](https://clawhub.ai/shawnshenopeninterx/skills/viral-video-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, plain-text console summaries, Python code snippets, and generated PDF reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEMORIES_API_KEY for transcript retrieval and may read Excel performance data for batch reports.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
