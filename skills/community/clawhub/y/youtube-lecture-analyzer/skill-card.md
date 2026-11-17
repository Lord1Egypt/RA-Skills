## Description:

Extracts and analyzes YouTube lecture subtitles to identify key points, evidence, and actionable insights for review, writing, and teaching purposes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wallfacer-web](https://clawhub.ai/user/wallfacer-web)

### License/Terms of Use:


## Use Case:

Learners, writers, and educators use this skill to fetch YouTube lecture subtitles and produce structured bilingual summaries, key questions, concepts, action items, and source-grounded takeaways.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local analysis reports can retain transcript content, including when a user expects summary-only behavior.

Mitigation: Avoid processing sensitive videos unless local transcript retention is acceptable, and delete generated lecture_analysis_<video_id>.txt files when they are no longer needed.

Risk: Transcript retrieval depends on a fixed local HTTP proxy.

Mitigation: Run the skill only in an environment where the local proxy is expected and trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wallfacer-web/skills/youtube-lecture-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Console text and local text report with structured markdown-style sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bilingual summaries and may write transcript-derived content to a local lecture_analysis_<video_id>.txt file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
