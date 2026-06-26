## Description: <br>
Delegate precise, formalizable computations and factual lookups to Wolfram|Alpha via its LLM API (HTTP) to get verified results and reduce arithmetic/modeling errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[firefrog-pepe](https://clawhub.ai/user/firefrog-pepe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Wolfram|Alpha for exact calculations, unit conversions, symbolic math, statistics, and structured factual lookups when concise model-readable results are needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and optional location or context fields are sent to Wolfram Alpha. <br>
Mitigation: Avoid secrets, private business data, and unnecessary location details in prompts and optional parameters. <br>
Risk: Responses are cached locally by default for repeated requests. <br>
Mitigation: Use --cache off for sensitive requests or when local result persistence is not acceptable. <br>
Risk: Query authentication can place the AppID in the request URL. <br>
Mitigation: Prefer the default bearer authentication mode. <br>


## Reference(s): <br>
- [Wolfram|Alpha LLM API Notes](references/llm-api.md) <br>
- [Full Results API Parameter Reference](references/full-api-params.md) <br>
- [Wolfram|Alpha LLM API Documentation](https://products.wolframalpha.com/llm-api/documentation) <br>
- [Wolfram|Alpha API Parameter Reference](https://products.wolframalpha.com/api/documentation?scrollTo=parameter-reference) <br>
- [ClawHub Skill Page](https://clawhub.ai/firefrog-pepe/wolfram-alpha-llm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text API responses with markdown guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and WOLFRAM_APP_ID; default response cap is 2500 characters and default cache TTL is 7 days.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
