## Description: <br>
Execute US and HK stock trades via Tiger Brokers API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[esanle](https://clawhub.ai/user/esanle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External traders and portfolio managers can use this skill to guide an agent through Tiger Brokers account checks and US or Hong Kong stock order workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to place live financial orders through Tiger Brokers. <br>
Mitigation: Use sandbox mode first, replace all example order values, and require explicit user confirmation before every order. <br>
Risk: The skill depends on Tiger Brokers account credentials and private key material. <br>
Mitigation: Store the private key with strict file permissions or a secret manager and avoid exposing real credentials in prompts or shared files. <br>


## Reference(s): <br>
- [Tiger Brokers 02800 quote page](https://www.itiger.com/hant/stock/02800) <br>
- [Tiger Brokers AAPL quote page](https://www.itiger.com/hant/stock/AAPL) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with Python and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tiger Brokers account configuration and private key material before use.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
