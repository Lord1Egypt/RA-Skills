## Description: <br>
Use when answering car maintenance, service interval, oil, brake fluid, tire pressure, or ownership questions through the TuhuCar CLI knowledge gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finiking](https://clawhub.ai/user/finiking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer vehicle maintenance and ownership questions by querying the TuhuCar CLI knowledge gateway and returning the gateway's markdown reply. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends car-care questions to the configured TuhuCar gateway, which could expose sensitive personal or vehicle details if an untrusted endpoint is used. <br>
Mitigation: Avoid sending sensitive personal details, verify the configured endpoint, and do not use an untrusted TUHUCAR_ENDPOINT. <br>
Risk: The skill depends on an external tuhucar CLI installation. <br>
Mitigation: Install only if you intend to use the TuhuCar CLI and verify the @tuhucar/cli or Homebrew package source before use. <br>


## Reference(s): <br>
- [TuhuCar CLI](https://github.com/tuhucar/cli) <br>
- [TuhuCar CLI Command Reference](references/command-reference.md) <br>
- [ClawHub package page](https://clawhub.ai/finiking/tuhucar-knowledge-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and parsed CLI replies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the TuhuCar CLI JSON envelope for parsing; presents data.reply as markdown and does not show raw JSON to the user.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
