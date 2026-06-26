## Description: <br>
Search for new services and make paid API requests using the x402 payment protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xRAG](https://clawhub.ai/user/0xRAG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search the x402 bazaar, inspect endpoint costs and schemas, and call paid x402 API endpoints with USDC on Base. Reviewers should treat paid calls and request payloads as sensitive because the skill can trigger real payments and transmit user-supplied data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger real paid USDC API calls. <br>
Mitigation: Use a limited-balance wallet, require explicit approval for each paid call, and always set --max-amount. <br>
Risk: An endpoint may have unexpected price, method, network, or schema requirements. <br>
Mitigation: Inspect payment requirements and input/output schemas before paying, then confirm the method, price, network, and request body. <br>
Risk: Request headers, query parameters, URLs, or JSON bodies may expose secrets or personal data to paid endpoints. <br>
Mitigation: Do not send secrets or personal data unless the user explicitly approves the exact endpoint and payload. <br>
Risk: Using npx awal@latest may execute a newer CLI version than the user reviewed. <br>
Mitigation: Verify or pin the Awal CLI version before use, especially in repeatable or production workflows. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/0xRAG/x402-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can guide an agent through x402 discovery, payment requirement inspection, and authenticated paid API calls through the Awal CLI.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
