## Description: <br>
Enable or disable an optional strict engineering workflow for coding tasks that emphasizes goal clarification, specs, planning, small implementation steps, and verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Spiceman161](https://clawhub.ai/user/Spiceman161) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to opt into a stricter coding workflow for build, debug, and implementation tasks, including short specs, plans, risk checks, stepwise execution, and final verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The mode persists until disabled, which can make later coding interactions more process-heavy than expected. <br>
Mitigation: Check the mode status before starting time-sensitive work and disable it when the stricter workflow is no longer needed. <br>
Risk: Optional notes in the mode state file could contain sensitive information. <br>
Mitigation: Avoid storing secrets, credentials, or private project details in the optional notes field. <br>


## Reference(s): <br>
- [Superpowers Mode on ClawHub](https://clawhub.ai/Spiceman161/superpowers-mode) <br>
- [Plan template](references/plan-template.md) <br>
- [Spec template](references/spec-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with short status confirmations and state-file instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a small persistent mode flag when enabled or disabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
