## Description:

小弟办公秘书团队 helps users manage schedules, draft and classify emails, organize documents, generate meeting minutes, and create mind maps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mx6315909](https://clawhub.ai/user/mx6315909)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and office-support users can use this skill to turn Chinese-language meeting notes, emails, schedules, and documents into organized drafts, minutes, task lists, formatted documents, and mind-map outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle sensitive meeting notes, emails, calendars, documents, memory, and session content.

Mitigation: Use a restricted workspace, redact sensitive inputs where possible, and review generated minutes, replies, schedules, and documents before sharing.

Risk: The requested tool access includes broad file writes, command execution, web search, memory, sessions, and scheduled tasks.

Mitigation: Disable broad exec, web_search, memory, session, and cron permissions unless each is specifically needed for the deployment.

Risk: Generated HTML mind maps may be opened or shared outside the agent environment.

Mitigation: Review generated HTML before opening or sharing it, especially when the input includes confidential content.

Risk: Live mailbox or calendar use could expose private communications or scheduling data without clear consent and scope.

Mitigation: Avoid live mailbox and calendar access until user consent, allowed accounts, retention, and task boundaries are defined.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, files, configuration, guidance]

**Output Format:** [Chinese text, Markdown, JSON status, DOCX files, and Mermaid, PlantUML, Markmap HTML, or Markdown mind maps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated meeting minutes, mind maps, and formatted documents under the skill workspace.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter and configs also contain 1.0.0, and architecture.json contains 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
