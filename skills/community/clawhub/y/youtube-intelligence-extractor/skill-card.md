## Description:

Extract structured intelligence from YouTube video transcripts for productivity, AI prompting, platform engineering, and creative workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erickgrau](https://clawhub.ai/user/erickgrau)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn YouTube URLs, video IDs, or pasted transcripts into actionable Markdown intelligence reports with todos, advice, runnable AI prompts, and engineering or creative insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use third-party transcript lookup services for YouTube content.

Mitigation: Avoid private or unlisted videos unless third-party lookup is disabled or the user explicitly accepts that exposure.

Risk: Fallback commands may install unpinned Python packages and alter the Python environment.

Mitigation: Review commands before execution and prefer an isolated environment with pinned package versions.

Risk: The artifact instructs agents to update the skill after improvements.

Mitigation: Remove or disable self-update behavior before normal use so skill files change only through reviewed releases.

Risk: Reports are saved automatically and may contain transcript-derived content or source metadata.

Mitigation: Confirm the output location and data handling expectations before processing sensitive videos or transcripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erickgrau/skills/youtube-intelligence-extractor)
- [Publisher profile](https://clawhub.ai/user/erickgrau)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown intelligence report with optional shell commands and saved Markdown file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include a video header, domain-specific extracted sections, top immediate actions, and source metadata when available.]

## Skill Version(s):

1.1.0 (source: release evidence and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
