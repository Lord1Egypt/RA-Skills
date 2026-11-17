## Description:

Evaluates agent skills with the Skill Reliability Level framework and produces scoring reports with improvement guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vuact](https://clawhub.ai/user/vuact)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill reviewers use this skill to assess a target skill's reliability, traceability, failure behavior, reproducibility, and operational risks before publication or reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags an unsafe shell pattern in documented examples that can turn reviewed skill content into command execution.

Mitigation: Use file-based JSON input and non-shell process invocation when running the analyzer, and avoid echoing untrusted JSON through a shell.

Risk: The skill reads target skill directories and writes evaluation reports.

Mitigation: Run it only on intended local skill directories and confirm output paths before report generation.

## Reference(s):

- [SRL Framework Reference](references/srl-framework.md)
- [SRL Scoring Criteria](references/scoring-criteria.md)
- [SRL Evaluation Template](assets/SRL-EVAL-TEMPLATE.md)
- [Skill Reliability Crisis Article](https://github.com/Vuact/Blog/blob/main/articles/Skill%20%E7%8B%82%E7%83%AD%E8%83%8C%E5%90%8E%EF%BC%8C%E6%B2%A1%E4%BA%BA%E5%91%8A%E8%AF%89%E4%BD%A0%E7%9A%84%E5%8F%AF%E9%9D%A0%E6%80%A7%E5%8D%B1%E6%9C%BA.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Structured JSON scoring data and Markdown or JSON SRL evaluation reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill expects reviewers to ground scores in file and line evidence, then uses a local Python script to calculate weighted scores and SRL levels.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
