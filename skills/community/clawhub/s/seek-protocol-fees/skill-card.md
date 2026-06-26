## Description: <br>
Analyze TokenJar profitability and optionally execute a Firepit burn-and-claim with preview-first checks, profitability math, simulation, and optional execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External DeFi users and developers use this skill to evaluate whether Uniswap TokenJar balances justify a Firepit burn and, after explicit confirmation, simulate or execute the burn-and-claim workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide irreversible wallet actions, including burning UNI and claiming assets. <br>
Mitigation: Use preview mode first, verify TokenJar and Firepit addresses, wallet, recipient, gas, and profitability math, then require fresh explicit confirmation before any burn or swap. <br>
Risk: Ambiguous confirmation could cause execution before the user has reviewed the exact burn and any swaps. <br>
Mitigation: Keep execution disabled unless the user clearly opts in and present the exact burn cost, selected assets, recipient, and post-burn swap plan before proceeding. <br>
Risk: DeFi transaction timing and race conditions can make profitability estimates stale. <br>
Mitigation: Run simulation and nonce freshness checks immediately before broadcast, and abort if Firepit state or expected profitability changes. <br>
Risk: A compromised or overfunded wallet could increase loss exposure. <br>
Mitigation: Prefer a limited-balance wallet and confirm the agent has only the funds needed for the intended operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/seek-protocol-fees) <br>
- [Skill specification](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown profitability reports with transaction status, asset breakdowns, and optional command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview mode is the default; execution requires explicit user confirmation and may include transaction links, final balances, and post-burn conversion details.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
