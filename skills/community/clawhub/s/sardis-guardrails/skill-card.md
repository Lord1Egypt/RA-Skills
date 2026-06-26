## Description: <br>
Real-time security monitoring and circuit breaker controls for Sardis agent wallets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EfeDurmaz16](https://clawhub.ai/user/EfeDurmaz16) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators responsible for Sardis agent wallets use this skill to check guardrail status, monitor spending and rate-limit alerts, and trigger or clear emergency wallet transaction stops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes emergency controls that can halt wallet transactions. <br>
Mitigation: Use the kill-switch commands only with authorized wallet access and after confirming the wallet ID and reason. <br>
Risk: The skill uses SARDIS_API_KEY for authenticated API requests. <br>
Mitigation: Store the API key in the environment, avoid pasting it into shared logs or prompts, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [Sardis homepage](https://sardis.sh) <br>
- [ClawHub skill page](https://clawhub.ai/EfeDurmaz16/sardis-guardrails) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and curl command examples plus JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SARDIS_API_KEY and command-line tools curl and jq.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
