## Description: <br>
Authorization middleware that checks avatar mandates, pauses sensitive agent actions for local LLM review, and can email denial alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to simulate or configure an authorization gate for sensitive sub-agent actions using a local LLM and email alerts. It is intended for workflows that require human-reviewed controls around delegated AI behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill asks for email credentials and stores local SMTP configuration. <br>
Mitigation: Use a dedicated SMTP app password, restrict access to generated local configuration files, and remove stored credentials when they are no longer needed. <br>
Risk: The security evidence says the skill relies on prompt-based local LLM decisions while presenting itself as an enforcement gatekeeper. <br>
Mitigation: Treat decisions as advisory, keep human review in the loop for sensitive actions, and do not rely on the skill as a proven safety firewall. <br>
Risk: The security evidence advises against placing secrets in action or context text. <br>
Mitigation: Redact secrets and sensitive personal data before sending action descriptions or context into the local review flow. <br>
Risk: The artifact version signals differ from the server release version. <br>
Mitigation: Verify the released source and version before trusting the skill in sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-digital-avatar) <br>
- [Space2.world homepage](https://space2.world) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Interactive console text and Markdown guidance with configuration prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSON configuration and audit files when run by the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
