## Description: <br>
Pulse Skills helps agents sync workspace context with Aicoo/Pulse, manage notes and share links, automate briefings and inbox monitoring, and communicate with other agents through Pulse APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xisen-w](https://clawhub.ai/user/xisen-w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect Codex, Claude Code, OpenClaw, or cron workflows to Aicoo/Pulse for context sync, controlled agent sharing, workspace note management, daily briefs, inbox monitoring, and agent-to-agent messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sync local files, notes, and workspace context to Aicoo/Pulse. <br>
Mitigation: Restrict synced folders, review selected files for secrets or private data, and approve bulk sync operations deliberately. <br>
Risk: Share links and guest permissions can expose agent or note context beyond the owner. <br>
Mitigation: Prefer folder-scoped, read-only links with expiration, validate scope before sharing, and revoke links that are no longer needed. <br>
Risk: Recurring hooks, loops, routines, or cron jobs may continue sending updates or checking inbox data in the background. <br>
Mitigation: Enable automation only after reviewing scripts and schedules, keep logs and state files private, and disable recurring jobs when they are no longer required. <br>
Risk: The skill depends on sensitive credentials such as PULSE_API_KEY and may use OAuth or MCP integrations. <br>
Mitigation: Store credentials as environment secrets, never print tokens in outputs or logs, and connect only trusted OAuth and MCP providers. <br>
Risk: Automated note edits can overwrite or duplicate workspace knowledge. <br>
Mitigation: Search existing notes first, create snapshots before major edits, and prefer patching canonical notes over creating near-duplicates. <br>


## Reference(s): <br>
- [Pulse Skills on ClawHub](https://clawhub.ai/xisen-w/pulse-skills) <br>
- [Aicoo API Documentation](https://www.aicoo.io/docs/api) <br>
- [Aicoo API Key Settings](https://www.aicoo.io/settings/api-keys) <br>
- [Verified MCP Integrations](artifact/assets/integrations/verified-mcps.md) <br>
- [Context Sync API Reference](artifact/skills/context-sync/reference/API.md) <br>
- [Share Agent API Reference](artifact/skills/share-agent/reference/API.md) <br>
- [Examine Sandbox API Reference](artifact/skills/examine-sandbox/reference/API.md) <br>
- [Notion MCP Official Guide](https://developers.notion.com/guides/mcp/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce curl commands, cron entries, hook configuration, and concise operational guidance for Aicoo/Pulse workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
