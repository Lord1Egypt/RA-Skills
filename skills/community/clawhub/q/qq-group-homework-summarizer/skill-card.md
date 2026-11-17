## Description:

Organizes QQ group homework for a selected date into an A4 Word document, preserving image attachments and optionally sending it by email or WeChat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laneovcc](https://clawhub.ai/user/laneovcc)

### License/Terms of Use:

MIT-0

## Use Case:

An assistant uses this skill to collect homework posts from one or more QQ groups for a selected date, format them as an A4 document, and optionally deliver the document by email or WeChat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports persistent changes to shared browser components and instructions that weaken sandbox isolation.

Mitigation: Install only when this workflow is specifically needed, and review its effects before use.

Risk: The security review reports actions that could disrupt unrelated browser windows or Word sessions.

Mitigation: Review the browser and Word actions before running the workflow, and avoid running it while those applications contain work that could be interrupted.

Risk: Inspection was incomplete: 7 of 8 components were scanned, with one partially inspected.

Mitigation: Review the remaining component and the partially inspected component before relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laneovcc/skills/qq-group-homework-summarizer)
- [api.md — QQ homework API reference](artifact/references/api.md)
- [troubleshooting.md — troubleshooting guide](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [A4 Word document (.docx), with optional PDF or text-only output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports image attachments, multiple groups, and subject filtering; can optionally send the document by email or WeChat.]

## Skill Version(s):

1.5.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
