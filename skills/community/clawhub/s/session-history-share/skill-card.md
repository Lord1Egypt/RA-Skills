## Description: <br>
Injects compressed summaries of previous OpenClaw sessions into new session bootstrap context for continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ouhaitao](https://clawhub.ai/user/ouhaitao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to preserve lightweight context across session resets by archiving recent session summaries and adding them to bootstrap context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prior conversation summaries may retain secrets, personal data, customer data, or unrelated project context and inject that content into later sessions. <br>
Mitigation: Install only when retained session context is intended; avoid sensitive sessions, review saved .session_history archives, and manually delete archives when they are no longer needed. <br>
Risk: The skill registers an OpenClaw bootstrap hook and scheduled cron task that change local agent behavior. <br>
Mitigation: Review the hook registration, cron job, and generated archives before relying on the skill; disable or remove the hook and cron task if the behavior is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ouhaitao/session-history-share) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown bootstrap content with local configuration and cron setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local session history archives and OpenClaw bootstrap hooks.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
