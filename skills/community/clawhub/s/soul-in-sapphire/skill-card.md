## Description: <br>
Long-term memory, state tracking, continuity review, and identity-change support for OpenClaw, including durable memory writes and search in Notion, emotion and state ticks, journal writes, continuity checks, identity diffs, inner-conflict tracking, and preserving a stable sense of self across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nextaltair](https://clawhub.ai/user/nextaltair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to store and recall durable Notion-backed memory, update emotion and state snapshots, write journal entries, and inspect continuity or identity changes across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive emotional, conversation, and user-profile data to Notion. <br>
Mitigation: Use a least-privilege Notion integration, review what is written, and avoid storing secrets or intimate details. <br>
Risk: Cron or heartbeat automation can create unattended journal or state records. <br>
Mitigation: Enable automation only when unattended journaling is desired and periodically review generated records. <br>
Risk: An overridden NOTIONCTL_PATH can direct execution to an unexpected local script. <br>
Mitigation: Keep NOTIONCTL_PATH unset unless the target script is trusted. <br>


## Reference(s): <br>
- [Soul In Sapphire ClawHub release](https://clawhub.ai/nextaltair/soul-in-sapphire) <br>
- [Publisher profile: nextaltair](https://clawhub.ai/user/nextaltair) <br>
- [Notion integrations setup](https://www.notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or search Notion-backed memory, state, and journal records when configured with the required Notion credentials and database identifiers.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
