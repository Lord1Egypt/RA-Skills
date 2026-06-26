## Description: <br>
Analyzes agent performance and suggests prompt, parameter, workflow, and strategy optimizations for iterative improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to profile agent callbacks, identify latency and resource bottlenecks, and compare optimization strategies for prompts, model parameters, and workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Profiling executes the supplied callback repeatedly, which can repeat side effects if the callback changes external systems or data. <br>
Mitigation: Profile idempotent callbacks, use safe test inputs, and reduce iteration counts before running callbacks that could perform irreversible actions. <br>
Risk: Optimization suggestions and generated prompt variants may not improve every agent or task. <br>
Mitigation: Evaluate proposed strategies against representative test cases before adopting them in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/yuyonghao-agent-self-improve) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [JavaScript API results and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns profiling summaries, bottleneck findings, optimization results, recommendations, and in-memory history.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
