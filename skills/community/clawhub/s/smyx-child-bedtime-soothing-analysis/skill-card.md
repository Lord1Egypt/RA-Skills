## Description:

Analyzes submitted child-bedroom audio and video for signs of bedtime distress and returns a report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and caregivers can use reports to review possible bedtime crying, fear-of-dark behavior, or nightmare waking from submitted audio and video. Independently verify any claimed monitoring or soothing behavior; the available security assessment does not establish those functions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Child-bedroom recordings and identity data may be handled by a remote service, and the service's data practices are not established here.

Mitigation: Verify the service, what recordings and identity data it receives, and the applicable data handling before submitting media.

Risk: The security assessment reports a mismatch between the claimed bedtime monitoring and soothing functions and the demonstrated capabilities; scanner coverage is partial.

Mitigation: Do not rely on the claimed monitoring or soothing behavior for child safety without independently confirming it; check whether export-only actions process media.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-child-bedtime-soothing-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown analysis report, optionally saved to a file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include an export link.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
