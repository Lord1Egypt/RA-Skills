## Description:

AI智能出题考试系统，可基于文档自动生成考试、指派学员并查询结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiangzidetiandi](https://clawhub.ai/user/xiangzidetiandi)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, training teams, and developers use this skill to upload documents, generate AI-assisted exams, assign exams to users or departments, and retrieve individual or batch exam results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends organization credentials, access tokens, uploaded documents, user and department lookups, and exam results to a configurable remote API.

Mitigation: Use only an approved HTTPS BASE_URL, limit credentials to the smallest required scope, and avoid confidential or regulated documents unless authorized.

Risk: Exam results and user or department lookup data may include sensitive personal or organizational information.

Mitigation: Restrict access to authorized operators and handle generated exams, assignments, and result outputs under the organization's data handling policy.

Risk: The artifact lists dependency ranges and no reviewed lockfile is provided in the evidence.

Mitigation: Review and pin dependencies or add a lockfile before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiangzidetiandi/skills/soke-ai-exam-skill)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, configuration values, and JSON-like result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload configured documents and send organization credentials, user or department identifiers, access tokens, and exam results to the configured remote API.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
