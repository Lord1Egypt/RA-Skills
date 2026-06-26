## Description: <br>
Generates production-ready Python Solana trading bots using Jupiter v6 API and DexScreener data with priority fees and secure key management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wterry57](https://clawhub.ai/user/Wterry57) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to draft Python Solana trading bot code, dependency manifests, and environment templates for strategies using Jupiter swaps and DexScreener market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated bots may automate live wallet-controlled trading without sufficient loss-limiting safeguards. <br>
Mitigation: Review generated code manually and run it first in dry-run, testnet, or with a dedicated low-balance wallet before using real funds. <br>
Risk: Trading code may expose users to unintended spend, slippage, or dependency risk if deployed as generated. <br>
Mitigation: Add hard spend limits, slippage bounds, explicit confirmation for live trades, dependency pinning, operational logs, and an emergency stop. <br>


## Reference(s): <br>
- [Jupiter v6 API endpoint](https://quote-api.jup.ag/v6) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [Markdown containing Python code, requirements, and environment template snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Typically includes generated main.py, requirements.txt, and .env template content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
