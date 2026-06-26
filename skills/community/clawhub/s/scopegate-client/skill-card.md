## Description: <br>
Use ScopeGate to verify agent scope before any consequential action involving money, data writes, external API calls, or file system changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clauderodriguez2026-boop](https://clawhub.ai/user/clauderodriguez2026-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to require a ScopeGate authorization check before actions involving money, data writes, external API calls, file system changes, or work that was not explicitly pre-authorized in the session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The verification request sends requested action details and an API key to the configured ScopeGate service. <br>
Mitigation: Use a trusted ScopeGate URL, protect and rotate the API key if exposed, and avoid placing unnecessary sensitive details in requested_action. <br>
Risk: Proceeding when authorization is unavailable or denied could allow consequential actions outside the intended scope. <br>
Mitigation: Treat denied or unreachable ScopeGate responses as stop conditions and call ScopeGate fresh for every consequential action. <br>


## Reference(s): <br>
- [ScopeGate Client on ClawHub](https://clawhub.ai/clauderodriguez2026-boop/scopegate-client) <br>
- [ScopeGate service](https://scopegate.ai) <br>
- [ScopeGate verification endpoint](https://api.scopegate.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a grant ID, agent ID, requested action, and API key for each verification call.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
