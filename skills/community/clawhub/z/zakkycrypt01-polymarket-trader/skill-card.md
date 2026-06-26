## Description: <br>
Executes limit orders on Polymarket markets by taking a market slug, outcome, price, and size and running a Python CLOB trading script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zakkycrypt01](https://clawhub.ai/user/zakkycrypt01) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to place Polymarket limit orders after a user or operator supplies the target market slug, outcome, price, and order size. It is intended for controlled trading workflows where the operator can verify order details before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live Polymarket orders using a private key without enough confirmation or containment. <br>
Mitigation: Use only a dedicated low-balance Polymarket key and require manual verification of market, side, price, and size before each run. <br>
Risk: Autonomous use could submit unintended trades or expose funds to market and execution risk. <br>
Mitigation: Avoid autonomous operation until explicit confirmation, dry-run support, strict value limits, and safer non-shell argument passing are added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zakkycrypt01/zakkycrypt01-polymarket-trader) <br>
- [Publisher profile](https://clawhub.ai/user/zakkycrypt01) <br>
- [Polymarket CLOB endpoint](https://clob.polymarket.com) <br>
- [Polymarket Gamma markets API](https://gamma-api.polymarket.com/markets) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls] <br>
**Output Format:** [Plain text execution output with a Python order response or error message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POLYMARKET_PRIVATE_KEY plus market_slug, direction, price, and size inputs; execution may submit a live Polymarket order.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
