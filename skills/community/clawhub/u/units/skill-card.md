## Description: <br>
Perform unit conversions and calculations using GNU Units. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Asleep123](https://clawhub.ai/user/Asleep123) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to convert measurements, calculate compound units, format numeric conversion results, and look up GNU Units definitions from an agent shell. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unquoted unit expressions or pasted shell syntax could be interpreted by the shell before GNU Units receives them. <br>
Mitigation: Quote unit expressions and avoid passing untrusted shell syntax to the command. <br>
Risk: Currency conversions may use stale static definitions from the local GNU Units data files. <br>
Mitigation: Treat currency results as estimates and verify exchange-sensitive calculations against a current financial source. <br>
Risk: Installing the required binary from an untrusted source could introduce package-level risk. <br>
Mitigation: Install GNU Units from a trusted package source such as the operating system package manager. <br>


## Reference(s): <br>
- [Units on ClawHub](https://clawhub.ai/Asleep123/units) <br>
- [Publisher profile: Asleep123](https://clawhub.ai/user/Asleep123) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and plain-text command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GNU Units to be installed; currency conversions may rely on stale local definitions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
