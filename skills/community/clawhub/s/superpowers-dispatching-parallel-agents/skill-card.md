## Description: <br>
Dispatch independent tasks to focused agents working concurrently on isolated problems without shared state or sequential dependencies for faster resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[demo112](https://clawhub.ai/user/demo112) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to split unrelated coding or investigation work into focused subagent tasks, dispatch them in parallel, and review the returned results before integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parallel agents may produce conflicting or incorrect changes if scopes overlap or results are integrated without review. <br>
Mitigation: Keep subagent tasks non-overlapping, review each returned summary and diff, and run tests before integrating work. <br>
Risk: Subagents may receive more context than needed for their task. <br>
Mitigation: Provide each subagent only the context, constraints, and expected output needed for its specific problem domain. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/demo112/superpowers-dispatching-parallel-agents) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with checklists and prompt examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Subagent tasks should remain independent and scoped to avoid conflicting edits.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
