## Description: <br>
Claude Session helps agents inspect, summarize, move, repair, archive, and delete Claude Code session files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to manage Claude Code session history, including finding session IDs, listing and searching transcripts, summarizing or analyzing sessions, moving sessions between projects, repairing broken JSONL structure, and cleaning up dead or obsolete sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, move, rewrite, delete, and persist sensitive Claude session history. <br>
Mitigation: Review target session IDs before use and avoid forwarding or storing transcripts that contain secrets, credentials, personal data, or proprietary work. <br>
Risk: State-changing workflows such as repair, destroy, migrate, purge, archive, classify --execute, and archive with RAG can alter or remove session data. <br>
Mitigation: Use dry-run or confirmation paths where available and back up important sessions before executing destructive or persistent operations. <br>
Risk: Import, summarize, analyze --sync, classify --execute, and RAG-related archive workflows may copy transcript content into other tools or stores. <br>
Mitigation: Limit these workflows to intended sessions and redact sensitive content before sharing or long-term persistence. <br>


## Reference(s): <br>
- [Claude Session on ClawHub](https://clawhub.ai/drumrobot/claude-session) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, tables, and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local scripts or MCP tools that inspect, move, rewrite, delete, or persist Claude session JSONL files.] <br>

## Skill Version(s): <br>
0.3.1 (source: release metadata and changelog, released 2026-06-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
