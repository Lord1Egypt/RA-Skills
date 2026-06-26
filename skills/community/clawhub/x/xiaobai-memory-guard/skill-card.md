## Description: <br>
Memory Guard helps agents check memory, note, reflection, and handoff files for continuity gaps, missing references, and stale session state before work begins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aptratcn](https://clawhub.ai/user/aptratcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add startup and periodic memory-continuity checks to long-running or restarted AI agent workflows. It is intended to surface missing handoff files, unreferenced addenda, stale memory records, and similar context-continuity issues before the agent proceeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release asks users to clone and automatically run an unpinned external Node script that is not included in the reviewed package. <br>
Mitigation: Review the referenced repository before installing, pin it to a trusted commit, and do not add startup hooks or cron jobs until the script's reads, writes, and logging are understood. <br>
Risk: Memory, note, reflection, and handoff files may contain sensitive operational details or credentials. <br>
Mitigation: Keep secrets and credentials out of memory files, handoff notes, reflections, and generated logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aptratcn/xiaobai-memory-guard) <br>
- [Publisher profile](https://clawhub.ai/user/aptratcn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and status-report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct an agent or operator to inspect memory, notes, reflections, handoff files, and git history before continuing work.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
