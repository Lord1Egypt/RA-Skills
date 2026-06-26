## Description: <br>
Buy Xcatcher points via x402 on Solana USDC, obtain an API key, create X crawl tasks, poll status, and download XLSX results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvpiggyqq](https://clawhub.ai/user/lvpiggyqq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users, remote agents, automation workflows, and analysts use this skill to buy Xcatcher service points, create X account crawl tasks, monitor completion, and download structured XLSX results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: USDC payment details can expire or be misread before payment. <br>
Mitigation: Use the live quote response for the recipient, amount, asset, and quote ID; refresh the quote if it expires. <br>
Risk: API keys and payment response files can expose access to the Xcatcher account. <br>
Mitigation: Avoid sharing terminal logs or buy.json when they contain an API key, and store credentials only in the intended local environment. <br>
Risk: Downloaded XLSX crawl results may contain sensitive data. <br>
Mitigation: Delete or secure task output files according to the user's data handling requirements. <br>


## Reference(s): <br>
- [Xcatcher Documentation](https://xcatcher.top/docs/) <br>
- [ClawHub Skill Page](https://clawhub.ai/lvpiggyqq/x402-x-tweet-fetcher) <br>
- [Publisher Profile](https://clawhub.ai/user/lvpiggyqq) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for API calls, payment verification, task polling, and XLSX result download handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
