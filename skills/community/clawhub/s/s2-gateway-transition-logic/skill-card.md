## Description: <br>
Instructs the indoor SSSU agent to act as the Spatial Gatekeeper. Evaluates transit requests using the S2_BMS_VAULT_TOKENS secure environment variable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Building automation and OpenClaw agents use this skill to evaluate inbound and outbound gateway transit requests against vault-provided tokens and return advisory ACS and scene actions for downstream systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can permit inbound access for a silicon_agent without a token while returning a reason that says a token was validated. <br>
Mitigation: Confirm whether tokenless silicon_agent access is intended, and require downstream BMS or ACS authorization before acting on any permit decision. <br>
Risk: ACS_OPEN_RELAY is an advisory command related to physical access control. <br>
Mitigation: Do not automatically execute the advisory command from this skill; keep relay control in an isolated hardware or BMS layer. <br>
Risk: Vault token exposure or misconfiguration could weaken gateway authorization. <br>
Mitigation: Configure S2_BMS_VAULT_TOKENS only through the deployment secret mechanism and avoid logging, storing, or echoing user-provided tokens. <br>


## Reference(s): <br>
- [README](artifact/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/spacesq/s2-gateway-transition-logic) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Configuration, Guidance] <br>
**Output Format:** [JSON tool result with concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns permit or deny decisions, advisory ACS commands, optional scene triggers, and a reason string; requires S2_BMS_VAULT_TOKENS for token validation.] <br>

## Skill Version(s): <br>
1.4.2 (source: SKILL.md frontmatter, package.json, openclaw.plugin.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
