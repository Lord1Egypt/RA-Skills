## Description: <br>
A ZetaChain helper that lets agents query omnichain balances, track CCTX status, and provide zEVM deployment and documentation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mango-ice-cat](https://clawhub.ai/user/mango-ice-cat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users working with ZetaChain use this skill to inspect wallet balances across ZetaChain, Ethereum, BSC, and Bitcoin, track cross-chain transaction status, and obtain practical zEVM development guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses and transaction hashes may be sent to public third-party RPC or blockchain API providers during lookup operations. <br>
Mitigation: Use only wallet addresses and transaction hashes that are acceptable to query through those providers. <br>
Risk: The skill may surface TSS or deposit addresses and suggested financial actions based on public chain data. <br>
Mitigation: Independently verify any TSS or deposit address and any financial action before moving funds. <br>
Risk: The helper depends on locally installed Python packages for execution. <br>
Mitigation: Install Python dependencies only from trusted package sources and review the script before running it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mango-ice-cat/zetachain-helper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON CLI output with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query public third-party RPC and blockchain API providers for balances, gas prices, and CCTX status.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
