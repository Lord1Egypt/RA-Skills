## Description: <br>
Analyzes complex planning problems with RALSTP to identify agents, dependencies, difficulty, and decomposition strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thedragosexperience](https://clawhub.ai/user/thedragosexperience) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, planners, and operations teams use this skill to analyze multi-actor workflows, resource contention, and orchestration problems with RALSTP concepts or optional PDDL domain/problem files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional formal mode reads local PDDL files supplied by path, so an incorrect path could expose unintended local planning data to the analysis output. <br>
Mitigation: Pass only the intended domain and problem files, and review the printed analysis before using it for planning decisions. <br>


## Reference(s): <br>
- [Road Traffic Accident Management PDDL instances](https://github.com/potassco/pddl-instances/tree/master/ipc-2014/domains/road-traffic-accident-management-temporal-satisficing) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown analysis with optional local shell command output from the PDDL analyzer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Conceptual mode analyzes natural-language problems; optional formal mode reads user-provided PDDL domain and problem files locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
