## Description: <br>
Coordinates a primary CEO agent that plans work, delegates tasks to worker agents, waits for their results, and summarizes final deliverables for the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moistenxx](https://clawhub.ai/user/Moistenxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they want a coordinating agent to decompose a request, choose long-running worker agents or one-off subagents, delegate work, and produce a consolidated report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Worker agents may receive task context through delegated prompts. <br>
Mitigation: Use trusted worker agents and avoid sharing secrets unless they are necessary for the task. <br>
Risk: Worker MEMORY.md files can retain stable preferences or methods beyond a single task. <br>
Mitigation: Periodically review worker MEMORY.md files and keep task data, client details, and credentials out of long-term memory. <br>


## Reference(s): <br>
- [Solo CEO ClawHub page](https://clawhub.ai/Moistenxx/solo-ceo) <br>
- [Employee SOUL template](references/employee_soul_template.md) <br>
- [Task plan template](references/plan_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with task plans, worker prompts, JSON configuration snippets, and final summary reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update worker MEMORY.md files when the agent records stable preferences or methods.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
