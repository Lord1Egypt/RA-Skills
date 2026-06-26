## Description: <br>
Perform complex mathematical calculations, physics simulations, data analysis, and scientific queries via the Wolfram|Alpha LLM API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Robert-Janssen](https://clawhub.ai/user/Robert-Janssen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to send mathematical, scientific, data, unit conversion, and factual quantitative queries to Wolfram|Alpha and receive exact API-backed answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to Wolfram Alpha with the configured WOLFRAM_APP_ID. <br>
Mitigation: Do not include secrets, private personal data, or confidential business information in queries unless sharing that information with Wolfram Alpha is acceptable for the use case. <br>
Risk: The skill depends on a configured API credential and network access to the Wolfram|Alpha API. <br>
Mitigation: Set WOLFRAM_APP_ID in the runtime environment and verify outbound access before relying on the skill in an agent workflow. <br>


## Reference(s): <br>
- [Wolfram|Alpha LLM API endpoint](https://www.wolframalpha.com/api/v1/llm-api) <br>
- [ClawHub release page](https://clawhub.ai/Robert-Janssen/wolfram-alpha) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text returned by the Wolfram|Alpha API, with setup and usage guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests package, and a WOLFRAM_APP_ID environment variable.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
