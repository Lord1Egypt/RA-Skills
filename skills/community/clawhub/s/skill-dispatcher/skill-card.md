## Description: <br>
Proactive skill router that helps an agent select and maintain installed skills through routing tables, enhancer checks, anti-forget gates, onboarding steps, and a coverage-check script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miantiao1231](https://clawhub.ai/user/miantiao1231) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route user requests to installed skills, detect uncovered skills, and maintain routing coverage as the skill set changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence broad, always-on routing behavior and persistent skill-maintenance state. <br>
Mitigation: Install it only when a global skill-routing layer is intended, and require explicit user approval before changing core rules, memory, routing tables, packaged skill files, or installed skills. <br>
Risk: The fallback protocol can direct an agent to search external registries when a local skill is not found. <br>
Mitigation: Disable external registry search unless the user explicitly requests it for the current task. <br>


## Reference(s): <br>
- [New Skill Onboarding Protocol](references/onboarding.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with routing tables, procedural guidance, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces routing decisions, onboarding steps, compliance tag guidance, and coverage reports through the bundled script.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
