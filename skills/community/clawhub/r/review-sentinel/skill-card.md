## Description:

Review Sentinel monitors, analyzes, and drafts responses to Google reviews for local businesses while tracking review changes in local state files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rolarenagent-cpu](https://clawhub.ai/user/rolarenagent-cpu)

### License/Terms of Use:

MIT-0

## Use Case:

External local business operators and their agents use this skill to monitor Google review changes, analyze reputation trends, draft human-reviewed responses, and generate reputation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs access to a Google Places API key for its primary review-fetching workflow.

Mitigation: Provide the key through GOOGLE_PLACES_API_KEY where possible, avoid storing credential files, and restrict who can access the runtime environment.

Risk: Local state and report files can contain business reputation data and review text.

Mitigation: Keep review-sentinel state and report folders private, and apply normal retention and access controls for customer-facing business data.

Risk: Drafted review responses may be unsuitable for public posting without business review.

Mitigation: Review every drafted response before posting, especially for negative reviews and privacy-sensitive businesses.

Risk: Recurring cron monitoring can repeatedly call external review services and store new snapshots.

Mitigation: Enable scheduled checks only when recurring monitoring is intended, and use a conservative cadence.

## Reference(s):

- [Review Sentinel ClawHub Page](https://clawhub.ai/rolarenagent-cpu/skills/review-sentinel)
- [Publisher Profile](https://clawhub.ai/user/rolarenagent-cpu)
- [State Schema](references/state-schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text, JSON summaries, and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GOOGLE_PLACES_API_KEY for Google Places API workflows; local review state and reports may be written under review-sentinel/.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
