## Description: <br>
Session History Enhanced helps developers add persistent, browsable, resumable OpenClaw chat session history with SQLite indexing, archive and restore workflows, pagination, and dashboard and chat-dropdown integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to add session archival, search, resume, rename, delete, pagination, and recent-session selection to an OpenClaw gateway dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delete flows can mislead users about whether chat transcripts are permanently deleted or archived. <br>
Mitigation: Review and align the confirmation text and deleteTranscript handling so each delete action clearly states whether transcript data will be kept, archived, or permanently removed. <br>
Risk: OpenClaw session history may contain private or important chat data. <br>
Mitigation: Review before installing, test on non-critical session data first, and consider recovery or soft-delete behavior before enabling destructive actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick-software/session-history-enhancements) <br>
- [Installation Guide](artifact/references/INSTALL.md) <br>
- [Backend History Database Reference](artifact/references/backend-history-db.ts.txt) <br>
- [Backend History Migration Reference](artifact/references/backend-history-migration.ts.txt) <br>
- [Backend Protocol Schemas Reference](artifact/references/backend-protocol-schemas.ts.txt) <br>
- [Backend RPC Handlers Reference](artifact/references/backend-rpc-handlers.ts.txt) <br>
- [Backend Session Archive Reference](artifact/references/backend-session-archive.ts.txt) <br>
- [Frontend Sessions Controller Reference](artifact/references/frontend-controllers-sessions.ts.txt) <br>
- [Frontend Sessions View Reference](artifact/references/frontend-views-sessions.ts.txt) <br>
- [Frontend State Changes Reference](artifact/references/frontend-state-changes.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript code references and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires reviewer application to an OpenClaw codebase and validation before use with private or important session data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, released 2026-02-27) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
