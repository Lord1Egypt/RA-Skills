## Description: <br>
Call 32 real-world APIs, including flights, hotels, weather, crypto prices, DeFi yields, stock quotes, web search, geocoding, IP reputation, blockchain data, code execution, and email, while paying per call in USDC on Base via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcelo-rowship](https://clawhub.ai/user/marcelo-rowship) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Agenthub to make paid, real-world data and utility API calls from an agent workflow, including travel lookup, market data, web search, weather, blockchain queries, remote code execution, and email sending. It is intended for users who can configure Node.js, npm, a dedicated Base wallet, and the AGENTHUB_WALLET_KEY credential. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize paid API calls from a configured Base wallet. <br>
Mitigation: Use a dedicated low-balance wallet for Agenthub and require explicit confirmation before each paid request. <br>
Risk: The email_send and code_exec APIs can trigger externally visible actions or run code in a remote service. <br>
Mitigation: Require separate user confirmation before using email_send or code_exec, and review the exact recipient, code, inputs, and expected cost before calling them. <br>
Risk: Requests may send prompts, URLs, code, or other data to an external SDK and gateway. <br>
Mitigation: Do not send secrets, private code, wallet credentials, or sensitive personal data through Agenthub unless the user has reviewed and accepted the data-sharing risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marcelo-rowship/rwagenthub) <br>
- [AgentHub gateway](https://agents-production-73c1.up.railway.app) <br>
- [rwagenthub-sdk npm package](https://www.npmjs.com/package/rwagenthub-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and JavaScript code blocks; API calls return JSON responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 20+, npm, AGENTHUB_WALLET_KEY, and a Base wallet funded with USDC for paid calls.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
