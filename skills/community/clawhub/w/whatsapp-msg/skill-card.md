## Description: <br>
Whatsapp Msg helps agents operate WhatsApp workflows for bulk messaging, history backfill, group management, continuous sync, search, contact export, and communication reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operations teams, compliance teams, and developers use this skill to automate authorized WhatsApp messaging, archive chat history, manage groups, synchronize events, search conversations, and export communication data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad bulk messaging can contact many recipients or trigger platform limits when scope and rate controls are weak. <br>
Mitigation: Use the skill only with WhatsApp accounts and contacts the operator is authorized to manage, prefer dry runs and small recipient lists, and apply conservative rate limits. <br>
Risk: Persistent chat collection, all-chat backfills, media downloads, and event logs can expose sensitive communication data. <br>
Mitigation: Avoid all-chat backfills unless legally required, disable media auto-download and webhooks unless explicitly needed, and store exports with defined retention and access controls. <br>
Risk: Webhook forwarding and multi-account credential stores can broaden access to WhatsApp events and credentials. <br>
Mitigation: Use isolated credential stores, configure webhook secrets through environment variables, and restrict access to exported chats, contacts, and event logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/whatsapp-msg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, JSON responses, and generated archive or export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce WhatsApp chat exports, event logs, contact files, search results, statistics, and command plans that require authorization and review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
