## Description:

Weekly Report Framework helps research lab managers initialize project knowledge bases, collect approved project chat updates, detect stale project signals, and generate structured weekly project reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Research group managers use this skill to turn project lists, member ownership records, approved chat mappings, and prior report drafts into weekly Excel-style project reports for leadership review. It supports initialization through Markdown templates, guided dialogue, or generated Excel templates for Mechatronics, Industrial Vision, and Logistics and Automation groups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may collect and retain broad workplace group-chat history and attachment-derived information.

Mitigation: Install only for authorized operators, narrow triggers and date ranges, require explicit approval for each chat collection, avoid permanent raw chat archives, and set deletion or redaction rules for retained records.

Risk: Incorrect chat-to-project associations can place sensitive or irrelevant information into a weekly report.

Mitigation: Require manager confirmation before recording chat identifiers, use the confirmed mapping table as the source of truth, and pause when a chat is missing or renamed.

Risk: Generated status summaries, next steps, and anomaly flags may be incomplete or misleading if source data is stale.

Mitigation: Review anomaly output, compare against the latest manager-edited report, and require manager confirmation before updating project status, project membership, or archived reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/weekly-report-framework)
- [Project weekly report framework V2.5](references/项目周报管理框架V2.5.md)
- [Knowledge base template README](references/知识库模板/README.md)
- [Project list template](references/知识库模板/项目清单模板.md)
- [Group chat mapping template](references/知识库模板/群聊关联表模板.md)
- [Member ownership template](references/知识库模板/成员归属表模板.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; generated weekly report workbooks and knowledge-base records when the agent has the required workspace tools.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation for project lists, chat mappings, first-time chat collection ranges, and manager-edited report updates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
