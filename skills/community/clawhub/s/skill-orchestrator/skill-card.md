## Description: <br>
Skill Orchestrator decomposes complex, multi-domain requests, discovers suitable skills, coordinates parallel or serial subtasks, manages checkpoints, and merges results into human-readable reports with optional JSON bundles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windymonkeys](https://clawhub.ai/user/windymonkeys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn complex requests into coordinated subtask plans, select local, marketplace, or fallback skills, track progress and checkpoints, and combine sub-results into a final answer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local skill discovery and optional memory lookup can expose local skill metadata or brief prior execution summaries. <br>
Mitigation: Keep configured skill and memory paths limited to trusted locations, and avoid storing secrets, full business content, or sensitive paths in execution summaries. <br>
Risk: Subtask coordination may pass task summaries and intermediate results between selected skills. <br>
Mitigation: Route only the minimum context needed for each subtask, review checkpoint prompts, and avoid delegating sensitive work to untrusted third-party skills. <br>
Risk: Direct-execution or bypass modes can increase the chance of unintended side effects for deployment, external, sensitive, or destructive work. <br>
Mitigation: Use confirmation checkpoints for high-risk tasks and avoid bypass modes when the task involves external side effects, sensitive data, or destructive operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/windymonkeys/skill-orchestrator) <br>
- [Project homepage](https://github.com/Windymonkeys/skill-orchestrator) <br>
- [Machine Contract](references/machine-contract.md) <br>
- [Skill Registry](references/skill-registry.md) <br>
- [Orchestration Engine](references/orchestration-engine.md) <br>
- [Execution Tracker](references/execution-tracker.md) <br>
- [Result Merger](references/result-merger.md) <br>
- [Human-in-the-Loop](references/human-in-the-loop.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown reports with optional JSON plan, event, and merge bundles] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include session IDs, step IDs, checkpoint prompts, progress summaries, conflict notes, and concise execution summaries.] <br>

## Skill Version(s): <br>
2.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
