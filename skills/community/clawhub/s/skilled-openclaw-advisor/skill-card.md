## Description: <br>
Queries a local SQLite FTS5 index of OpenClaw documentation to answer configuration, CLI, channel, provider, plugin, session, agent, protocol, and troubleshooting questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanford](https://clawhub.ai/user/seanford) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to build and query a local documentation index before answering OpenClaw configuration, CLI, integration, and troubleshooting questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The updater can send update metadata to a hard-coded Telegram recipient. <br>
Mitigation: Review `scripts/update_index.py` before installation and do not run it unless that notification behavior is acceptable. <br>
Risk: Documentation understates access to OpenClaw configuration. <br>
Mitigation: Assume scripts may read `~/.openclaw/openclaw.json` for skill configuration and review local config contents before running indexing or query commands. <br>
Risk: The release has a suspicious security verdict from server evidence. <br>
Mitigation: Review and scan the skill before deployment, following the security guidance from the release evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seanford/skilled-openclaw-advisor) <br>
- [Query Guide](references/query-guide.md) <br>
- [Skills Data Directory Convention](SKILLS_DATA_CONVENTION.md) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown and plain text with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit compact agent-mode search results, human-readable answers, detailed references, index status, and update diffs.] <br>

## Skill Version(s): <br>
1.4.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
