## Description: <br>
Sift instructs agents to request signed authorization receipts from a third-party governance service before consequential tool calls such as file writes, API calls, browser actions, external posts, and financial transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[walkojas-boop](https://clawhub.ai/user/walkojas-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Sift to add prompt-layer authorization checks before agents perform consequential actions. The skill is intended for workflows that need signed allow or deny receipts, audit trails, policy checks, and fail-closed handling when the Sift service is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides prompt-layer governance and should not be treated as a hard enforcement boundary by itself. <br>
Mitigation: Use a platform-level plugin or other deterministic enforcement layer when actions must be blocked independently of agent instruction-following. <br>
Risk: Authorization requests may involve private signing keys or sensitive action parameters. <br>
Mitigation: Keep the private signing key out of chat and logs, and send only the minimum sensitive details needed for authorization. <br>
Risk: The skill depends on a third-party Sift account and authorization service before consequential actions proceed. <br>
Mitigation: Install it only when third-party authorization checks are intended, and maintain fail-closed behavior when Sift is unreachable or returns a non-ALLOW response. <br>


## Reference(s): <br>
- [Sift ClawHub release page](https://clawhub.ai/walkojas-boop/skill-sift) <br>
- [Sift API account and onboarding endpoint](https://api.sift.walkosystems.com) <br>
- [Sift authorization endpoint](https://api.sift.walkosystems.com/authorize) <br>
- [Sift challenge endpoint](https://api.sift.walkosystems.com/auth/challenge) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON and HTTP request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Sift account, tenant credentials, agent identity, nonce challenge, and ed25519 request signature before authorization checks can be submitted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
