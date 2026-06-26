## Description: <br>
Convert units for length, weight, temperature, data, and speed. Use when switching measurement systems, sizing storage, or adjusting recipe quantities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users can use this skill to convert length, weight, temperature, speed, data storage, and time values from a shell-style unit converter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted input values can make the bundled shell script run local commands. <br>
Mitigation: Review before installing. Only use trusted numeric inputs unless the script is fixed to validate numbers and pass values to awk safely, for example through awk variables rather than constructed awk source. <br>


## Reference(s): <br>
- [Unitconv on ClawHub](https://clawhub.ai/xueyetianya/unitconv) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text with converted numeric values and units] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses awk-backed calculations; security evidence warns to use only trusted numeric inputs unless input validation is fixed.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
