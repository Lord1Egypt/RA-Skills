## Description: <br>
Detects when a user may be referring to information from another session and asks for permission before searching shared memory or recent session history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoquan](https://clawhub.ai/user/guoquan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to recover relevant context from shared memory or recent sessions when a request appears to depend on prior conversation history. It is intended to ask for confirmation before searching or syncing findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may surface private conversation history or shared-memory content during cross-session recall. <br>
Mitigation: Approve searches only when prior-session recall is intended, and review any displayed findings before using or syncing them. <br>
Risk: Sensitive details could be copied into shared memory if a sync is approved without review. <br>
Mitigation: Do not approve syncing passwords, API keys, private messages, or other sensitive details; redact sensitive content before any memory write. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoquan/session-sync-detect) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown prompts, search result summaries, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose memory or session-history searches only after user confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, package.json, and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
