## Description: <br>
Uses the Futu paper trading API to query quotes, account funds, positions, orders, fills, historical market data, and financial reports, and to place or cancel simulated orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XXXWANG](https://clawhub.ai/user/XXXWANG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to let an agent inspect Hong Kong market data and manage a Futu paper-trading workflow. It supports account checks, quote and financial-data queries, simulated buy and sell orders, order review, fills review, and order cancellation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place and cancel simulated orders through a Futu paper-trading account. <br>
Mitigation: Keep FutuOpenD in simulation mode and require explicit user approval before buy, sell, or cancel commands. <br>
Risk: Trade unlock credentials may be needed for order operations. <br>
Mitigation: Provide trade passwords only through trusted local environment settings and avoid storing account passwords in files. <br>
Risk: First run installs unpinned Python packages and some financial-data commands may use AkShare-backed external sources. <br>
Mitigation: Review dependency resolution before deployment and treat external financial-data responses as third-party data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/XXXWANG/xtrade-futu-paper-trade) <br>
- [FutuOpenD download and support](https://www.futuhk.com/en/support/topic1_464) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses from CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful commands return ok and data fields; failures return an error field and may include next_steps guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
