## Description: <br>
Toggle is a context layer that fetches ToggleX work-session, project, focus-score, and context-switch data so an agent can summarize activity, answer recall questions, and offer proactive workflow suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aleksandar-jive](https://clawhub.ai/user/aleksandar-jive) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use Toggle to retrieve recent ToggleX activity history, generate concise work digests, recall prior sessions, detect stale projects or context switching, and suggest next steps based on observed routines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retrieves and may locally persist detailed work-activity history, including projects, domains, focus scores, session timing, and workflow descriptions. <br>
Mitigation: Enable it only where local memory storage is acceptable, restrict access to persisted files, and confirm how to delete stored data before using background sync. <br>
Risk: Cron or background sync can continue collecting activity history after setup. <br>
Mitigation: Require clear user opt-in for scheduled syncs, document the refresh cadence, and use the skill state setting to disable cron checks or background collection when the user declines. <br>
Risk: Raw workflow descriptions may include sensitive URLs, internal paths, or tokens. <br>
Mitigation: Paraphrase activity descriptions by default, avoid echoing raw URLs or raw workflow payloads unless explicitly requested, and review output before sharing it outside the local agent context. <br>
Risk: Proactive nudges, predictions, and automation suggestions can be incorrect or overreach based on incomplete activity history. <br>
Mitigation: Frame suggestions as optional, require user confirmation before creating automations or cron jobs, and back off when the user dismisses predictions or nudges. <br>
Risk: The skill depends on a Toggle API key for access to personal activity data. <br>
Mitigation: Store the API key only in the configured environment or agent config, never paste it into chat, and rotate it if access is no longer needed or appears compromised. <br>


## Reference(s): <br>
- [ToggleX Homepage](https://x.toggle.pro) <br>
- [ToggleX OpenClaw Integration](https://x.toggle.pro/new/clawbot-integration) <br>
- [ToggleX Workflows API Endpoint](https://ai-x.toggle.pro/public-openclaw/workflows) <br>
- [ClawHub Skill Page](https://clawhub.ai/aleksandar-jive/toggle) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON API responses, Markdown summaries or memory sections, and inline shell/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and TOGGLE_API_KEY; may persist fetched activity data into local memory files when requested or scheduled.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact frontmatter lists 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
