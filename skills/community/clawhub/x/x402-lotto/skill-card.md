## Description: <br>
Accesses x402.lotto lottery services to list lotteries, fetch jackpots, purchase tickets, check ticket status, and retrieve draw results through the x402 payment protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanemort1982](https://clawhub.ai/user/shanemort1982) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents can use this skill to interact with x402.lotto lottery endpoints, including jackpot lookup, ticket purchase, ticket status checks, and result retrieval. It is intended for wallet-backed x402 payment workflows involving USDC on Base. <br>

### Deployment Geography for Use: <br>
Global, subject to local lottery, gambling, and payment regulations. <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables wallet-backed USDC ticket purchases without clear spending limits, price checks, or user confirmation safeguards. <br>
Mitigation: Use only a dedicated low-balance or test wallet, require visible pricing and explicit confirmation before any ticket purchase or USDC payment, and verify the x402.lotto service and @x402/evm dependency before use. <br>
Risk: Lottery participation and payment handling may be restricted by location. <br>
Mitigation: Confirm that lottery participation and related USDC payments are legal in the user's jurisdiction before installing or executing the skill. <br>


## Reference(s): <br>
- [x402 Lotto ClawHub release](https://clawhub.ai/shanemort1982/x402-lotto) <br>
- [x402.lotto service](https://x402.lotto) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents through wallet configuration, x402 payment wrapping, and lottery API requests.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
