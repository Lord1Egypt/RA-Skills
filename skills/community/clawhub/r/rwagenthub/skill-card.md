## Description:

Agenthub lets agents call 32 paid real-world APIs for travel, weather, markets, web search, geocoding, IP reputation, blockchain data, code execution, and email using USDC payments on Base via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcelo-rowship](https://clawhub.ai/user/marcelo-rowship)

### License/Terms of Use:


## Use Case:

External developers and agent users use Agenthub to call paid data and utility APIs from an agent, including search, travel, market data, blockchain, code execution, and email workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a wallet key and paid API calls, so unintended calls can spend funds.

Mitigation: Use a dedicated low-balance wallet and assume every API call may incur a USDC charge.

Risk: The skill installs third-party Node code before making gateway calls.

Mitigation: Review the SDK package and install path before use, and do not run the documented shell snippet as-is until the install pattern is hardened.

Risk: The code_exec API can process submitted code and may expose sensitive inputs.

Mitigation: Do not send secrets, wallet credentials, proprietary code, or confidential data through code_exec.

Risk: The email_send API can send messages with real-world side effects.

Mitigation: Confirm recipients and message content manually before sending email.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marcelo-rowship/skills/rwagenthub)
- [AgentHub Gateway](https://agents-production-73c1.up.railway.app)
- [AgentHub SDK on npm](https://www.npmjs.com/package/rwagenthub-sdk)
- [AgentHub API Endpoint](https://agents-production-73c1.up.railway.app/v1/call)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with bash and JavaScript snippets; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls may incur USDC charges and require Node.js, npm, AGENTHUB_WALLET_KEY, and a Base wallet with USDC.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
