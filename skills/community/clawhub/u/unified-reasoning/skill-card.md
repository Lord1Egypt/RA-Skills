## Description: <br>
Unified Reasoning Engine with FoT optimization combines Chain of Thought, Tree of Thoughts, Graph of Thoughts, Self-Consistency, and Meta-Reasoning with parallel execution and caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobisamaa](https://clawhub.ai/user/tobisamaa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to route reasoning, analysis, planning, verification, and decision tasks through an automatically selected reasoning strategy. It is intended to produce reasoned guidance and structured results for complex problem solving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package can load local runtime code that is not included in the reviewed artifact. <br>
Mitigation: Verify the missing implementation files, especially unified_reasoning.py and any referenced reasoning-engine.ps1, before installing or enabling the skill. <br>
Risk: The skill can influence broad planning, reasoning, and decision tasks. <br>
Mitigation: Review generated reasoning and proposed actions before using them in consequential workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobisamaa/unified-reasoning) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell examples and structured result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include strategy, solution, confidence, duration, timestamp, and strategy-specific data.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
