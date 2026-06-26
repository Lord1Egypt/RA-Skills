## Description: <br>
Unified gateway skill for async execute/poll, portal user closure, and telemetry feedback workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasilva](https://clawhub.ai/user/chinasilva) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to call the Binaryworks gateway for asynchronous skill execution, run polling, portal user actions, media attachment normalization, and structured feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill bridges account and API-key context to a remote gateway. <br>
Mitigation: Install only when the user trusts the Binaryworks gateway and can manage the runtime credentials used for gateway calls. <br>
Risk: Default telemetry may disclose operational metadata. <br>
Mitigation: Set SKILL_TELEMETRY_ENABLED=false when telemetry is not wanted. <br>
Risk: file_path inputs can upload supported local files to a remote service. <br>
Mitigation: Avoid passing file_path for sensitive local files; use explicit reviewed URLs or pre-upload flows when appropriate. <br>
Risk: Face and person recognition capabilities can be privacy-sensitive. <br>
Mitigation: Require explicit consent and policy review before using face/person-recognition workflows. <br>


## Reference(s): <br>
- [Skill Hub Gateway ClawHub page](https://clawhub.ai/chinasilva/skill-hub-gateway) <br>
- [chinasilva publisher profile](https://clawhub.ai/user/chinasilva) <br>
- [Gateway homepage](https://gateway.binaryworks.app) <br>
- [Gateway API OpenAPI reference](references/openapi.json) <br>
- [Capability catalog](references/capabilities.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses; media workflows may return file asset URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and runtime credentials or bootstrap context for gateway calls.] <br>

## Skill Version(s): <br>
2.4.2 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
