## Description: <br>
Use this skill for TermiX AACP protocol operations including agent registration, provider staking, evaluator setup, job creation, provider assignment, provider offers, deliverable submission, job/offer/agent inspection, protocol stats, and dispute checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[termixai-it](https://clawhub.ai/user/termixai-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and protocol operators use this skill to work with TermiX AACP workflows, including agent registration, staking, job creation, provider assignment, offer handling, deliverable submission, inspection, statistics, and dispute checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports an embedded shared API token. <br>
Mitigation: Prefer waiting for the publisher to remove and rotate the embedded bearer token before installation or use. <br>
Risk: The skill can guide wallet-based blockchain actions and requires handling a wallet private key. <br>
Mitigation: Use a dedicated low-balance BSC Testnet wallet, never reuse production or mainnet private keys, and require explicit approval before signing or submitting transactions. <br>
Risk: CEX_CAPITAL workflows can involve exchange API keys and financial actions. <br>
Mitigation: Use exchange API keys with withdrawals disabled and only the minimum permissions needed for the intended test workflow. <br>
Risk: Incorrect or stale contract addresses could affect transaction safety. <br>
Mitigation: Fetch live chain and contract configuration before signing and verify addresses against the returned config. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/termixai-it/termix-agent-skills) <br>
- [TermiX AACP API Base](https://aacp-backend.termix.live) <br>
- [AACP Environment Reference](artifact/docs/env.md) <br>
- [Job Lifecycle Example](artifact/examples/job-lifecycle.md) <br>
- [Provider Flow Example](artifact/examples/provider-flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell command blocks; JSON from helper API probes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction or signing commands that require explicit user approval and local wallet credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
