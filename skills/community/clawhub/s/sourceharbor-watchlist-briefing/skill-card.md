## Description:

Use SourceHarbor watchlists, briefings, Ask, MCP, and HTTP API to answer one question with current story context and evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and developers use this skill to inspect one SourceHarbor watchlist through MCP or a local HTTP API, answer one operator question with current story context and evidence, and recommend a next action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path asks users to run external SourceHarbor code without a pinned revision in the artifact.

Mitigation: Use a pinned, reviewed SourceHarbor revision or signed release before connecting it to an agent runtime.

Risk: The capability map includes report-sending and workflow actions that go beyond a read-only watchlist briefing.

Mitigation: Run the MCP server with minimal permissions and prefer a read-only SourceHarbor role unless report sending or workflow execution is explicitly intended.

Risk: A partial MCP or HTTP connection can leave the agent without enough evidence to answer the operator question.

Mitigation: Require the agent to state runtime gaps clearly and avoid filling missing watchlist, briefing, or evidence data with guesses.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/xiaojiou176/skills/sourceharbor-watchlist-briefing)
- [README](artifact/README.md)
- [SourceHarbor Skill References](artifact/references/README.md)
- [SourceHarbor MCP And HTTP Setup](artifact/references/INSTALL.md)
- [SourceHarbor Capability Map](artifact/references/CAPABILITIES.md)
- [OpenHands / OpenClaw Demo Walkthrough](artifact/references/DEMO.md)
- [SourceHarbor Troubleshooting](artifact/references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured briefing fields and inline command or configuration snippets when setup is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected fields include current_story, what_changed, evidence_used, suggested_next_action, and runtime_gap when access is partial.]

## Skill Version(s):

1.0.0 (source: server release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
