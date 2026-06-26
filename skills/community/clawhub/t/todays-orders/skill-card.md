## Description: <br>
Use this skill when the user wants a single approved onchain order for a Solana wallet, one explicit forbidden order, a quote-backed execution preview, or a receipt-backed daily debrief powered by OKX OnchainOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richard7463](https://clawhub.ai/user/richard7463) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to analyze one Solana wallet and produce a disciplined daily onchain plan: one approved action, one forbidden action, and a quote-backed execution preview before any approved broadcast. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce transaction-oriented guidance for irreversible on-chain activity. <br>
Mitigation: Review the wallet address, amount, asset pair, route, slippage, and expected output before approving any broadcast. <br>
Risk: A preview could be mistaken for an executed transaction. <br>
Mitigation: Treat outputs as previews until a user-approved broadcast returns a confirmation receipt. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richard7463/todays-orders) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fixed section order with wallet posture, approved action or no-action stance, forbidden action, execution preview, and debrief.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
