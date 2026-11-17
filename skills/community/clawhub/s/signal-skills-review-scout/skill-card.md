## Description:

Mine user reviews for whatever kind of product this repo actually is (mobile app, browser extension, web/SaaS) and turn them into ranked findings — pain points, regressions, feature-request clusters, praise worth keeping. Use when the user asks what reviews/feedback say, wants a release-quality check against real user complaints, or asks "what are people saying about the app."

This skill is ready for commercial/non-commercial use.

## Publisher:

[orensegal](https://clawhub.ai/user/orensegal)

### License/Terms of Use:

MIT-0

## Use Case:

Product teams and developers use this skill to turn compliant user review sources into ranked findings about bugs, regressions, feature requests, and praise. It can also compare review patterns with known issues or product analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags possible private analytics access beyond the skill's review-analysis purpose.

Mitigation: Use analytics only when needed, and verify and authorize the backend, project, and data before querying.

Risk: The scan is partial, with two referenced paths unresolved, so it does not establish all behavior.

Mitigation: Review the unresolved paths and relevant behavior before enabling the skill in a sensitive environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, JSON, HTML reports, Markdown reports, Shell commands]

**Output Format:** [Ranked review findings and regression notes, with HTML or Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are grouped by theme and version, with empty categories marked explicitly.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
