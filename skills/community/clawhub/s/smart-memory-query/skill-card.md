## Description: <br>
Enforce proactive, query-optimized memory_search usage. Must run memory_search when (1) prior context is referenced, (2) a new task starts, or (3) a proper noun appears. Build short 2-4 token queries by splitting intent to avoid empty AND-based FTS results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jo-minjun](https://clawhub.ai/user/jo-minjun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agent users and developers use this skill to make an agent consult saved memory before new tasks, prior-context questions, or named-project work. It helps the agent form short, focused memory_search queries and retry with a key proper noun when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface sensitive, stale, or irrelevant saved memories more often because it encourages broad proactive memory searches. <br>
Mitigation: Review stored memories periodically and remove content that should not be reused in routine tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jo-minjun/smart-memory-query) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jo-minjun) <br>


## Skill Output: <br>
**Output Type(s):** [guidance] <br>
**Output Format:** [Markdown instructions with example memory_search calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs the agent to run short, split memory_search queries before relevant work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
