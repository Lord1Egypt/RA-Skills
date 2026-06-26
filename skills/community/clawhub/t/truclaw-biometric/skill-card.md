## Description: <br>
Biometric guardrail for OpenClaw. Intercepts dangerous tool calls and requires Face ID verification via TruClaw iOS app before execution. Biometric processing is on-device only. A relay (Cloudflare Worker, source included) handles push delivery and JWT exchange. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanjaymk908](https://clawhub.ai/user/sanjaymk908) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to require biometric approval before sensitive tool calls such as shell commands, file changes, network sends, or message and financial actions are allowed to proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a privileged external plugin and sensitive identity enrollment. <br>
Mitigation: Review the exact npm and GitHub plugin sources before installing, and enroll only after confirming the identity and biometric data handling model is acceptable. <br>
Risk: Tool-call details and approval metadata may pass through third-party services. <br>
Mitigation: Prefer a self-hosted relay for sensitive work and avoid using the shared relay around secrets until its filtering, storage, and transmission behavior is reviewed. <br>
Risk: The skill requires a sensitive Anthropic API key. <br>
Mitigation: Use a dedicated, revocable API key scoped to this integration. <br>


## Reference(s): <br>
- [TruClaw source repository](https://github.com/sanjaymk908/trukyc-openclaw) <br>
- [TruClaw relay source](https://github.com/sanjaymk908/trukyc-openclaw/tree/main/cloudflare-worker) <br>
- [Truclaw Biometric on ClawHub](https://clawhub.ai/sanjaymk908/truclaw-biometric) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with inline configuration and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TruClaw iOS app enrollment, TRUKYC_RELAY_URL, and ANTHROPIC_API_KEY_TRUKYC.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
