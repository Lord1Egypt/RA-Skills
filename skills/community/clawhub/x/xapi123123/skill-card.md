## Description: <br>
Use xapi CLI to access real-time external data: Twitter/X profiles, tweets, and timelines, crypto token prices and metadata, web search, news, and AI text processing such as summarization, rewriting, chat, and embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Glacier-Luo](https://clawhub.ai/user/Glacier-Luo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover and call xapi CLI actions for external data retrieval, third-party API access, and AI text processing. It is useful when a workflow needs structured JSON responses from Twitter/X, crypto, web search, news, or supported API gateway services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route agent requests through a broad external API gateway, including third-party API proxies. <br>
Mitigation: Install only when the user trusts xapi.to and the npx xapi-to package, and review each target service before sending data. <br>
Risk: Commands may involve OAuth binding, posting, write methods, or payment top-up flows. <br>
Mitigation: Require explicit human approval before OAuth binding, posting, POST/PUT/PATCH/DELETE calls, or any top-up/payment flow. <br>
Risk: The xapi API key can be stored locally or provided through XAPI_API_KEY. <br>
Mitigation: Protect the stored API key, avoid exposing local xapi configuration, and do not send secrets or confidential content through the gateway. <br>


## Reference(s): <br>
- [xapi homepage](https://xapi.to) <br>
- [ClawHub skill page](https://clawhub.ai/Glacier-Luo/xapi123123) <br>
- [Publisher profile](https://clawhub.ai/user/Glacier-Luo) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON command inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The xapi CLI returns JSON by default; API keys may be supplied through XAPI_API_KEY or local xapi configuration.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
