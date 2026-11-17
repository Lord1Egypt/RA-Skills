## Description:

Find students who haven't submitted artifacts by matching filenames against a class manifest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericli98](https://clawhub.ai/user/ericli98)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, teaching assistants, or course operations staff use this skill to compare a class manifest CSV against an artifact folder or filename list and identify students with missing submissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submission checks can expose student IDs, names, filenames, and missing-submission status.

Mitigation: Install and run the skill only where the operator is authorized to view class manifests and submission filenames; keep manifests and results in private locations.

Risk: Filename-based matching can produce missed or incorrect matches when filenames omit expected codes or names.

Mitigation: Review the reported missing and submitted lists before acting on them, and choose the match field that matches the class naming convention.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ericli98/skills/submit-check)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ericli98)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports total students, submitted count, missing count, missing students, and matched submissions when available.]

## Skill Version(s):

1.0.1 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
