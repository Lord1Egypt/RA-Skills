## Description: <br>
CLI tool for the QuantMap distributed computing protocol. Manages node setup, task execution, and result submission on devnet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChatRichAi](https://clawhub.ai/user/ChatRichAi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and node operators use this skill to install and run the QuantMap devnet CLI for wallet setup, node registration, task execution, validation, coordination, and status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and relies on the external @alphify/qmap-client npm package. <br>
Mitigation: Install only after reviewing and trusting the npm package and its release metadata. <br>
Risk: The CLI creates a local signing identity and stores files under ~/.qmap. <br>
Mitigation: Use a separate devnet identity and protect local ~/.qmap files from disclosure or unintended sharing. <br>
Risk: Worker, validator, and coordinator commands perform signed devnet network actions and may consume devnet compute. <br>
Mitigation: Run these commands only in an environment where devnet task execution and signed network actions are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChatRichAi/qmap-client) <br>
- [Skill homepage](https://clawhub.com/skills/qmap-client) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target the QuantMap devnet profile and may create local identity files under ~/.qmap.] <br>

## Skill Version(s): <br>
0.1.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
