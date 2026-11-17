## Description:

Buy Xcatcher points via x402 on Solana USDC, obtain an API key, create X crawl tasks, poll status, and download XLSX results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvpiggyqq](https://clawhub.ai/user/lvpiggyqq)

### License/Terms of Use:


## Use Case:

External users, agents, automation workflows, and analysts use this skill to purchase Xcatcher points, create X account crawl tasks, monitor task status, and retrieve structured XLSX results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends payment proof, X usernames, task metadata, and API credentials to xcatcher.top.

Mitigation: Install and run it only if that data sharing is acceptable for the intended use case, and handle PAYMENT-SIGNATURE and XCATCHER_API_KEY as secrets.

Risk: The paid workflow can spend Solana USDC and the artifact lacks clear confirmation guardrails before payment or external actions.

Mitigation: Confirm the live quote amount, payment destination, and requested crawl scope before sending any USDC or creating tasks.

Risk: The workflow can print and save issued API keys and purchase responses in local files such as buy.json.

Mitigation: Avoid printing secrets, restrict local file access, and remove sensitive response files after extracting required values.

## Reference(s):

- [Xcatcher Documentation](https://xcatcher.top/docs/)
- [X402 X Tweet Fetcher on ClawHub](https://clawhub.ai/lvpiggyqq/skills/x402-x-tweet-fetcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands and guidance for paid x402 requests, API-key handling, Xcatcher task management, and XLSX result downloads.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
