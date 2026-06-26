## Description: <br>
Get Portland transit information including arrivals, trip planning, and alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjrussell](https://clawhub.ai/user/mjrussell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and transit-focused agents use this skill to answer Portland-area bus, MAX, train, arrival, trip-planning, and service-alert questions through the TriMet CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a TriMet API key through TRIMET_APP_ID. <br>
Mitigation: Keep TRIMET_APP_ID private and avoid exposing it in prompts, logs, shell history, or shared outputs. <br>
Risk: Trip planning can involve exact home, work, or other sensitive addresses. <br>
Mitigation: Use stop IDs, landmarks, or less precise locations when exact addresses are not necessary. <br>
Risk: The skill depends on a globally installed trimet-cli package. <br>
Mitigation: Confirm trimet-cli is the intended npm package before installation or execution. <br>


## Reference(s): <br>
- [TriMet](https://trimet.org) <br>
- [TriMet Developer API](https://developer.trimet.org/) <br>
- [ClawHub skill page](https://clawhub.ai/mjrussell/trimet) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mjrussell) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the trimet CLI and TRIMET_APP_ID environment variable.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
