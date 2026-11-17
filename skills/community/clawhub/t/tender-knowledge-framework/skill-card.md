## Description:

Tender Knowledge Framework helps agents organize tender-analysis knowledge for interpreting bid documents, preparing proposals, analyzing evaluation methods, identifying contract risks, and maintaining industry case notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ylbwjf](https://clawhub.ai/user/ylbwjf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, procurement teams, and bidding specialists use this skill to guide agents that summarize tender requirements, structure bid-preparation checklists, compare scoring methods, and produce recurring learning reports for tender strategy work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring internet-learning tasks may run on a schedule without clear user control or stop conditions.

Mitigation: Use the skill in a user-triggered workflow or require confirmation before each internet-learning run.

Risk: The skill may persist local knowledge files in memory/tender-learning/ and tender-knowledge-framework/ directories.

Mitigation: Require confirmation before writes to those directories and review generated files before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ylbwjf/skills/tender-knowledge-framework)
- [Publisher profile](https://clawhub.ai/user/ylbwjf)
- [Tender document interpretation knowledge](artifact/knowledge/01-招标文件解读.md)
- [Bid document preparation knowledge](artifact/knowledge/02-投标文件编制.md)
- [Evaluation method analysis knowledge](artifact/knowledge/03-评标办法分析.md)
- [Learning report template](artifact/report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance, report templates, checklists, and structured knowledge notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask an agent to perform recurring internet-learning tasks and write local tender-learning files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
