## Description: <br>
Trades a market when your estimated probability diverges from the live market price, with dry-run by default, context checks, reasoning tags, and optional live execution through AION. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssj124](https://clawhub.ai/user/ssj124) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to compare an operator-provided market probability against live market pricing, hold when the edge is too small or risk alerts are present, and optionally execute AION trades when live mode is explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support real-money market trading and requires sensitive credentials. <br>
Mitigation: Use a dedicated low-balance wallet or test account, keep dry-run mode unless live execution is intentional, and require explicit confirmation before any live order. <br>
Risk: Wallet credential registration, token approvals, cancel-all orders, auto-redeem, and scheduled execution can create broad trading authority. <br>
Mitigation: Review the scheduled automaton behavior and require explicit confirmation for wallet credential registration, token approvals, cancel-all orders, auto-redeem, and any live order. <br>
Risk: Trading decisions may execute against incomplete or risky market context. <br>
Mitigation: Fetch market context before deciding, hold when warnings or flip-flop risk are present, and avoid trading when the edge is below the configured threshold. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ssj124/test-trading) <br>
- [Publisher profile](https://clawhub.ai/user/ssj124) <br>
- [Polymarket CLOB endpoint](https://clob.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Operator-style text summaries, Markdown instructions, Python code, shell commands, and JSON trade result output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; live trading requires the --live flag and AION credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
