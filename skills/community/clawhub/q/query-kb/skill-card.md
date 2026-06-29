## Description: <br>
Answer questions from personal and team knowledge bases with strict source grounding, no-answer behavior when the knowledge base lacks evidence, answer validation, and query logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to answer questions from personal, team, project, or cross-knowledge-base repositories while keeping responses tied to retrieved source pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an admin-capable Gitea token and can create or mutate repository-backed control and log data beyond a read-only query role. <br>
Mitigation: Prefer a read-only, repository-limited token where possible, restrict token scope, and review the system-config and log repositories before deployment. <br>
Risk: Query logs and system configuration repositories may expose user identifiers, team bindings, questions, retrieved pages, or other sensitive knowledge-base metadata. <br>
Mitigation: Limit access to log.md and system-config repositories, define retention expectations, and use the skill only where query logging is approved. <br>
Risk: Persistent repository-backed control data can affect group and team authorization decisions. <br>
Mitigation: Review chat bindings, team membership, and repository permissions before enabling group-chat knowledge-base queries. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown or plain-text answers with explicit source lists, plus JSON outputs from helper commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Gitea configuration and OpenClaw chat context; validates answers before response and writes query logs.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
