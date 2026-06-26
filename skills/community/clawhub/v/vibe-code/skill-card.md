## Description: <br>
Discipline skill for vibe-driven development that helps agents turn mood, feel, and outcome-shaped software requests into scoped, runnable work without drift, hallucinated APIs, or silent scope creep. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhauga](https://clawhub.ai/user/jhauga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill when a collaborator describes software by mood, comparison, or intended outcome rather than a precise specification. It establishes a Vibe Lock, ships one runnable slice, and confirms scope before expanding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vague or aesthetic requests can expand into silent scope creep. <br>
Mitigation: Require an explicit Vibe Lock with Feel, Outcome, Out of scope, and Stack before generating code. <br>
Risk: The agent may invent packages or APIs to match a requested feel. <br>
Mitigation: Use only dependencies the agent can identify with confidence, or ask the collaborator to confirm the package choice. <br>
Risk: Generated examples may accidentally reuse real names, emails, or business data from the prompt context. <br>
Mitigation: Replace prompt-derived real data with placeholder examples before committing generated docs or code. <br>
Risk: Repo-maintenance and package installation commands can have broad effects if executed without review. <br>
Mitigation: Review commands before execution and use narrower options such as dry-run or no-yolo modes when available. <br>


## Reference(s): <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional code, shell command, and configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a four-line Vibe Lock before code generation and a single runnable slice before further feature work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
