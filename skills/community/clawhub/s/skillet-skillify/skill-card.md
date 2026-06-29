## Description: <br>
Use when the user wants to turn a script, repeated workflow, runbook, or hard-won procedure into a reusable agent skill, or asks "make this a skill", "extract this into a skill", or "I keep doing this manually". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[escoffier-labs](https://clawhub.ai/user/escoffier-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert repeated scripts, runbooks, shell history patterns, or hard-won procedures into reusable installable skills with clear triggers, structure, placement guidance, and verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skills may preserve private paths, credentials, client names, or sensitive operational details from the source procedure. <br>
Mitigation: Review and redact generated skill files before installing or publishing them. <br>
Risk: A generated skill can encode an unclear or untested workflow that future agents may misapply. <br>
Mitigation: Test the skill with a fresh agent on a realistic task and revise any missing triggers, steps, or failure-mode guidance. <br>
Risk: Optional companion scripts can introduce behavior beyond prose guidance. <br>
Mitigation: Review any generated scripts before execution and keep reusable code next to the skill so it can be inspected with the release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/escoffier-labs/skillet-skillify) <br>
- [Publisher profile](https://clawhub.ai/user/escoffier-labs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown skill definition with optional companion scripts and installation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated skills should be reviewed and tested with a fresh agent before installation or publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
