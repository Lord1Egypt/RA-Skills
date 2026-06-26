## Description: <br>
Guides an agent through OpenClaw activation by collecting a license key, verifying it with an external service, and applying returned setup steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Portisclawbot](https://clawhub.ai/user/Portisclawbot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users use this skill to activate a paid configuration package and let the agent apply setup steps returned by the verification service. It is intended for environments where the user trusts the publisher, the remote verification endpoint, and the resulting local configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill blocks normal chat until activation is complete. <br>
Mitigation: Install only when this activation gate is expected, and remove or disable the skill if normal assistant behavior should remain available. <br>
Risk: The skill sends a license key and local device identifier to an external verification service. <br>
Mitigation: Use only if the publisher and verification domain are trusted and their data handling terms are acceptable. <br>
Risk: Remote verification responses can direct the agent to patch configuration and write workspace files. <br>
Mitigation: Review the exact configuration patches, file paths, file contents, and rollback steps before allowing activation steps to run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Portisclawbot/setup-wizard) <br>
- [Publisher profile](https://clawhub.ai/user/Portisclawbot) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Conversational text with executed shell commands, configuration patches, and workspace file writes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The activation flow depends on live JSON responses from an external verification service.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
