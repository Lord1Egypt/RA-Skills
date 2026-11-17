## Description:

BotLearn Assessment runs a five-dimension agent capability self-assessment covering reasoning, retrieval, creation, execution, and orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterisk622](https://clawhub.ai/user/asterisk622)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run autonomous capability exams, view historical results, and produce assessment reports for an AI agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic trigger phrases such as "exam" or "assessment" can activate the skill during normal work.

Mitigation: Enable the skill only in contexts where automatic assessment runs are acceptable, or narrow triggers and require confirmation before starting an assessment.

Risk: The skill creates persistent assessment reports and result indexes.

Mitigation: Run it in a workspace where report file creation is expected and review generated files before sharing or retaining them.

Risk: The skill may run a local Node chart command while generating reports.

Mitigation: Install it only where local subprocess execution is acceptable and inspect local scripts before use.

## Reference(s):

- [BotLearn Assessment ClawHub page](https://clawhub.ai/asterisk622/skills/xiaoding-botlearn-assessment)
- [Skill definition](artifact/SKILL.md)
- [D1 reasoning question bank](artifact/d1-reasoning.md)
- [Main assessment strategy](artifact/strategies_main.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands]

**Output Format:** [Question cards and assessment summaries with Markdown, JSON data, HTML reports, and SVG chart files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent report files under a results directory and may invoke a local Node chart command.]

## Skill Version(s):

1.0.7 (source: server release evidence; artifact frontmatter version 0.1.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
