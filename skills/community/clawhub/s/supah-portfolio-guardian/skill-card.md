## Description: <br>
Automated wallet monitoring with real-time alerts. Track portfolio value, detect suspicious transactions, monitor approvals, and get risk warnings across Base and EVM chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supah-based](https://clawhub.ai/user/supah-based) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to monitor public wallet addresses, check portfolio risk, review watched wallets, and request health or rebalance guidance across Base and EVM chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes real-time portfolio protection, but security evidence says it should be treated as on-demand monitoring rather than guaranteed real-time protection. <br>
Mitigation: Use results as advisory signals and verify time-sensitive wallet activity, approvals, and transactions with trusted wallet or blockchain tools before acting. <br>
Risk: Wallet addresses and portfolio queries are sent to SUPAH and related providers, and watched wallet addresses are stored locally. <br>
Mitigation: Use only with public addresses you are comfortable sharing, and review or delete ~/.supah-guardian-state.json when monitoring is no longer needed. <br>
Risk: Security guidance flags the x402 payment path as unclear. <br>
Mitigation: Confirm x402 payment behavior, recipient, network, and per-call costs before enabling automatic paid calls. <br>


## Reference(s): <br>
- [SUPAH Portfolio Guardian on ClawHub](https://clawhub.ai/supah-based/supah-portfolio-guardian) <br>
- [SUPAH API](https://api.supah.ai) <br>
- [SUPAH Website](https://supah.ai) <br>
- [x402](https://www.x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON results from command-line actions, with brief text errors and cost messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, curl, and SUPAH_API_BASE; makes outbound requests to api.supah.ai; stores watched wallet state locally in ~/.supah-guardian-state.json.] <br>

## Skill Version(s): <br>
1.3.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
