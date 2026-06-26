## Description: <br>
Text transformation, regex, diff, format conversion, and JSON manipulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CutTheMustard](https://clawhub.ai/user/CutTheMustard) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to transform generated text, run regex and diff operations, convert Markdown or HTML, and parse or format JSON through a stateless text API. It is intended for agent-generated content unless the user explicitly asks to send their text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive or user-provided text could be sent to an external service without clear consent. <br>
Mitigation: Use the skill on agent-generated content by default and only send user text after explicit user instruction. <br>
Risk: External API availability, rate limits, or paid-tier costs can affect completion. <br>
Mitigation: Confirm the service is appropriate for the task and account for the free-tier limit or x402 paid usage before repeated calls. <br>


## Reference(s): <br>
- [Text Transform service](https://text.agentutil.net) <br>
- [ClawHub skill page](https://clawhub.ai/CutTheMustard/text-transform) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [JSON API responses and transformed text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [External stateless API; ask before sending non-agent-generated text.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
