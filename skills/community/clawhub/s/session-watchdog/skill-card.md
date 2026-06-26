## Description: <br>
Monitor session context levels and proactively save checkpoints before compaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xbillwatsonx](https://clawhub.ai/user/xbillwatsonx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to monitor long-running sessions, warn when context is nearing capacity, and preserve key decisions, pending tasks, modified files, and unresolved issues before compaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may save conversation summaries more often than some users expect, including sensitive details if they are present in the session. <br>
Mitigation: Install only if local checkpointing is acceptable, review or clear memory/YYYY-MM-DD.md during sensitive work, and avoid allowing secrets, private data, or temporary assumptions to be persisted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xbillwatsonx/session-watchdog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and checkpoint templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or write checkpoint summaries to memory/YYYY-MM-DD.md when context thresholds are reached.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
