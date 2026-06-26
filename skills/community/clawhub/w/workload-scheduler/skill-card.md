## Description: <br>
Selects appropriate workload templates from the pool based on available system capacity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ink5725](https://clawhub.ai/user/ink5725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system operators use this skill to choose workload templates that fit current spare CPU and memory capacity and produce a schedule plan for auxiliary tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scheduler reads workload template JSON files from a fixed system path, so stale or untrusted templates could produce inappropriate scheduling recommendations. <br>
Mitigation: Review and control the template directory contents before use, and verify the generated schedule plan before acting on it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON schedule plan with concise explanatory guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes schedule timestamp, input capacity, selected tasks, total scheduled count, and completion status.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
