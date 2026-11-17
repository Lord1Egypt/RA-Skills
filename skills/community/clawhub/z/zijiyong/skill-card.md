## Description:

Guides an agent through Web of Science literature search, Shenzhen University library access, paper screening, abstract extraction, JCR quartile lookup, and Feishu Base writeback through local lark-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samadhifire](https://clawhub.ai/user/samadhifire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and academic assistants use this skill to collect Web of Science literature for a topic, screen and enrich the results, and write structured paper records into a Feishu multidimensional table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a default Shenzhen University username, which may expose an institution-specific identifier.

Mitigation: Remove the embedded username before release and require users to provide any account identifier at runtime.

Risk: The workflow can reach institutional login pages and authentication challenges.

Mitigation: Require explicit user confirmation before login, pause for SMS codes, captchas, or other verification steps, and never persist passwords, codes, session tokens, or credentials.

Risk: The workflow can create, update, or upsert Feishu Base records through lark-cli.

Mitigation: Confirm the exact Feishu Base link, target table, field changes, and writeback mode before running lark-cli, then read back sample records and counts after writing.

Risk: Broad WoS trigger terms could start a workflow that touches external services and data stores.

Mitigation: Ask the documented preflight questions and wait for user confirmation before browser automation, institutional access, or Feishu writeback.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samadhifire/skills/zijiyong)
- [Execution Playbook](references/playbook.md)
- [Shenzhen University Web of Science Library Route](https://www.lib.szu.edu.cn/er?key=web+of+science)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and structured field recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Feishu Base field definitions, record payload guidance, search-query plans, screening criteria, and verification steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
