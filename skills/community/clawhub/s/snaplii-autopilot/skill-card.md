## Description: <br>
Snaplii Autopilot helps an agent buy a Snaplii gift card, redeem it through a browser session, and complete a merchant or delivery order after required user confirmations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snapliiai](https://clawhub.ai/user/snapliiai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill when they want an agent to complete a Snaplii-funded purchase or food delivery order end to end. The agent checks Snaplii Cash balance, quotes and purchases a gift card, redeems it in a browser session, and stops for confirmation before purchase and final order placement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can complete purchases using the user's Snaplii balance and browser session. <br>
Mitigation: Install only when this behavior is intended, and require explicit user confirmation before the gift-card purchase and again before the final merchant order. <br>
Risk: Order details such as merchant, amount, delivery address, tip, and final total may be wrong if not reviewed. <br>
Mitigation: Show the full order summary and have the user review each detail before clicking the final order or pay button. <br>
Risk: Gift-card redemption codes and PINs are sensitive payment credentials. <br>
Mitigation: Enter redemption details only into the merchant site and avoid posting them in chat unless the user asks. <br>


## Reference(s): <br>
- [Snaplii Autopilot on ClawHub](https://clawhub.ai/snapliiai/snaplii-autopilot) <br>
- [snapliiai publisher profile](https://clawhub.ai/user/snapliiai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with tool and browser-action steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Snaplii CLI or Snaplii MCP tools plus an available browser-automation tool.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
