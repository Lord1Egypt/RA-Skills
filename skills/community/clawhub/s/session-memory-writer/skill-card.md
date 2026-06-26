## Description: <br>
Write structured task outcome blocks to memory/YYYY-MM-DD.md at session end, with consistent formatting for Langfuse backfill, Quill journal generation, and QMD search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to append structured local task outcomes, session summaries, and OUTBOX entries after agent work. It helps preserve consistent memory records for later search, journal generation, and observability workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task details and technical decisions may be retained in persistent local memory or OUTBOX files. <br>
Mitigation: Review generated memory and OUTBOX entries in sensitive projects, and install the skill only when persistent local task logging is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/session-memory-writer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown task blocks and OUTBOX entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Append-only local memory entries using fixed headers and required fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
