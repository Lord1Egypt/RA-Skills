## Description:

Analyzes supplied surveillance videos for virtual fence crossings and returns structured safety reports and historical results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers use the skill to review home monitoring videos for movement across configured safety boundaries and retrieve prior analysis reports. It supports safety review while human supervision remains necessary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analysis may not provide an immediate alert when an infant approaches a hazard.

Mitigation: Do not rely on the skill for time-critical supervision; maintain direct human monitoring and physical safeguards.

Risk: Video may undergo external processing, with possible account or identity handling.

Mitigation: Review the processing and account implications before installing the skill or sharing footage.

Risk: The security assessment is incomplete because a referenced local path could not be resolved.

Mitigation: Review the skill and its dependencies before installing.

## Reference(s):

- [API documentation](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-virtual-fence-intrusion-warning-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured analysis report; historical report lists use Markdown tables, with JSON detail available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include monitoring results, warnings, recommendations, timestamps, screenshots, and report links.]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata; artifact frontmatter lists 1.0.26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
