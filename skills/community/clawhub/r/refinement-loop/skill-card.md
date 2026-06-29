## Description: <br>
Design and run iterative generate→critique→revise loops optimized for Claude Opus 4.8, with thinking-as-critic, cost controls, and model routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prometheus-prime](https://clawhub.ai/user/prometheus-prime) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, prompt engineers, and agent builders use this skill to design refinement loops that improve generated outputs through explicit criteria, critique, revision, convergence checks, and cost controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Refinement loops can send sensitive documents or private data to external AI model providers. <br>
Mitigation: Avoid sending sensitive data unless the provider account settings, terms, and data-handling expectations permit it. <br>
Risk: Multi-pass AI loops can exceed intended token or cost budgets. <br>
Mitigation: Set token and cost limits before running a loop, log token usage per pass, and stop when limits are reached. <br>
Risk: Weak rubrics or soft critique can converge on incorrect or misleading guidance. <br>
Mitigation: Use explicit evaluation criteria, objective checks where possible, a separate critic role, and human review for high-impact outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/prometheus-prime/refinement-loop) <br>
- [Prometheus-prime publisher profile](https://clawhub.ai/user/prometheus-prime) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code] <br>
**Output Format:** [Markdown with prompt templates, tables, and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable files; includes cost-control, model-routing, and convergence guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
