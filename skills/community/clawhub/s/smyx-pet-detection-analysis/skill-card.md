## Description:

Detects cats, dogs, and birds in a target area using video or images for home pet monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Home pet owners use the skill to detect and count cats, dogs, and birds in submitted images or video, and to view previous analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media analysis and remote report features may handle sensitive household footage or report data.

Mitigation: Review the service and report handling before use, and submit only media and report queries the user intends to share.

Risk: The skill initializes an internal account identity and uses account or token handling for remote analysis and history lookups.

Mitigation: Review identity and credential handling before installation; keep internal identifiers and credentials out of user-facing output.

Risk: History lookup and report export features extend beyond detecting pets in provided media.

Mitigation: Use history lookup or report export only when requested, and confirm the account's report data is appropriate to access.

## Reference(s):

- [Pet detection API reference](references/api_doc.md)
- [Analysis API details](skills/smyx_analysis/references/api_doc.md)
- [Skill usage demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown]

**Output Format:** [Structured JSON analysis results, text reports, and Markdown report lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include detected counts, category statistics, confidence summaries, and report links.]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
