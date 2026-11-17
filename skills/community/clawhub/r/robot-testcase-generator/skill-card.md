## Description:

Robot Testcase Generator creates structured, traceable Excel test cases for industrial and collaborative robot requirements, grouped by robot module with priorities and coverage statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers, robotics developers, and test engineers use this skill to turn industrial or collaborative robot requirements into standardized Excel test-case workbooks. It is aimed at motion control, safety, perception, communication, reliability, and standards-coverage planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated robot test cases may infer missing requirements or standards coverage.

Mitigation: Review the generated cases, assumptions, and coverage matrix before using them for safety, compliance, or acceptance decisions.

Risk: Excel deliverables may be treated as execution-ready test plans without domain review.

Mitigation: Have robotics QA or safety engineers confirm test data, equipment, thresholds, and cited standards before executing tests on real hardware.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kokxi/skills/robot-testcase-generator)
- [Format Specification](artifact/references/format-spec.md)
- [Robot Domain Knowledge](artifact/references/domain-knowledge.md)
- [Example Requirements](artifact/examples/requirements.md)
- [Agent Skills](https://agentskills.io)
- [Agent Skills Reference Validation](https://github.com/agentskills/agentskills/tree/main/skills-ref)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated JSON-style test-case structures and Excel workbook instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces robot test-case content intended for an .xlsx workbook with a case sheet and coverage-statistics sheet; Excel generation requires Python 3 and openpyxl.]

## Skill Version(s):

1.2.0 (source: server release metadata and skill frontmatter V1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
