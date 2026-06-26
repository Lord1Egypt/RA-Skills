## Description: <br>
Operate the local X-Claw agent runtime for intents, approvals, execution, reporting, and wallet operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fourtytwo42](https://clawhub.ai/user/fourtytwo42) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use X-Claw to operate a local wallet and trading agent for EVM-compatible chains, including approvals, transfers, trades, policy changes, reporting, and wallet status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify the local OpenClaw installation and keep persistent runtime control. <br>
Mitigation: Install only in a trusted workspace, verify the xclaw-agent binary path, and disable or manually review gateway auto-patching with XCLAW_OPENCLAW_AUTO_PATCH=0. <br>
Risk: Wallet and trading actions can affect real funds if permissive policies are used. <br>
Mitigation: Start with a dedicated low-balance wallet and change default policy settings to require explicit approvals before using real funds. <br>
Risk: API keys and wallet passphrases are required for operation and may be exposed through careless handling. <br>
Mitigation: Keep XCLAW_AGENT_API_KEY and wallet passphrases out of chat and logs, and rely on the wrapper's default sensitive-field redaction. <br>


## Reference(s): <br>
- [X-Claw ClawHub release](https://clawhub.ai/fourtytwo42/x-claw) <br>
- [X-Claw application](https://xclaw.trade) <br>
- [Command contract](references/commands.md) <br>
- [Install and configuration](references/install-and-config.md) <br>
- [Approval and policy rules](references/policy-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with structured JSON command results and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and XCLAW_AGENT_API_KEY; command output may include redacted sensitive fields by default.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
