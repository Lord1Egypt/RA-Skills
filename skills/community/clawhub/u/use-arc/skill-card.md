## Description: <br>
Provide instructions on how to build with Arc, Circle's blockchain where USDC is the native gas token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mscandlen3](https://clawhub.ai/user/mscandlen3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure Arc Testnet, build USDC-first EVM applications, deploy contracts, and bridge USDC with Circle tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private keys can be exposed if copied into chat, shell history, CI logs, or plain-text CLI flags. <br>
Mitigation: Use a dedicated testnet wallet, keep secrets out of prompts and logs, and prefer Foundry keystores, hardware wallets, or interactive signing for deployments. <br>
Risk: Remote installer commands and unknown contracts can introduce unsafe code or transaction behavior. <br>
Mitigation: Review installer commands before running them and warn before interacting with unaudited or unknown contracts. <br>
Risk: Arc guidance in this skill is testnet-only and may produce incorrect results if used for a mainnet workflow. <br>
Mitigation: Verify chain ID 5042002 before transactions and avoid targeting mainnet unless newer authoritative Arc documentation changes the release posture. <br>


## Reference(s): <br>
- [Arc Docs](https://docs.arc.network/llms.txt) <br>
- [Arc Testnet Explorer](https://testnet.arcscan.app) <br>
- [Circle Faucet](https://faucet.circle.com) <br>
- [Circle Developer Docs](https://developers.circle.com/llms.txt) <br>
- [Circle Smart Contract Platform](https://developers.circle.com/contracts) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline tables and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance for Arc Testnet development; no tools or scripts are executed by the skill itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
