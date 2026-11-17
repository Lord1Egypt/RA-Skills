## Description:

Analyzes supplied pet videos for behavior or distress indicators through a remote service and returns structured reports or report history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners use the skill to submit supported videos for behavior analysis, review structured reports, and retrieve earlier reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is rated suspicious and is reported to perform remote video analysis, with possible account creation and persistent identity or token storage.

Mitigation: Review and accept those data-handling behaviors before installing; avoid use if they are not acceptable.

Risk: Scanner coverage was partial and imported implementations could not be verified, so the evidence does not establish the full behavior.

Mitigation: Review the complete skill and imported implementations before relying on its behavior.

## Reference(s):

- [API interface documentation](artifact/references/api_doc.md)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-pet-calming-trigger-analysis)
- [Skill demonstration page](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Structured analysis report text with JSON content; report history is returned as JSON content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts MP4, AVI, or MOV videos up to 10 MB; analysis reports may include a report link.]

## Skill Version(s):

1.0.21 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
