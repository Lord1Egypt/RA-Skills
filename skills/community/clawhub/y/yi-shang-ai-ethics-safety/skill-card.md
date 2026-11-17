## Description:

Provides AI ethics audit helpers for authenticity monitoring, alienation-pattern detection, value-alignment checks, and 27-type personality matrix guidance based on Instinctual Integrity Quotient theory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxfei420](https://clawhub.ai/user/zxfei420)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI governance reviewers use this skill to inspect AI responses for authenticity, over-compliance, manipulation, KPI-driven behavior, and value-alignment signals before manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate safety-monitoring capability while relying on fragile heuristics and fixed or fail-open scores.

Mitigation: Treat its reports as review prompts, not automated approval decisions, and manually verify findings against the underlying AI output.

Risk: Running a prototype ethics-audit aid directly in a host environment can create unnecessary dependency and file-output exposure.

Mitigation: Review dependencies first, run the scripts in an isolated environment, and provide only intended text inputs and output directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxfei420/skills/yi-shang-ai-ethics-safety)
- [AI 树德理论框架](artifact/references/theory.md)
- [AI 三商测评指南](artifact/references/equality_measurement.md)
- [AI 三商人格分类矩阵](artifact/references/personality_matrix.md)
- [AI 树德论文](https://blog.csdn.net/Figo_Cheung/article/details/159044535)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, Python helper code examples, and concise textual guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit report files can be written to a user-specified output directory.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
