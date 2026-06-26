## Description: <br>
Analyze sentiment of text or URLs. Supports batch analysis, emotion detection, comparative and trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to classify sentiment, emotions, intensity, reasoning, and confidence for individual text, fetched URLs, or batches of up to 10 inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided text or fetched URL content to external AIProx, LightningProx, or Claude infrastructure. <br>
Mitigation: Avoid submitting secrets, regulated data, or private customer content unless provider terms are acceptable for the use case. <br>
Risk: The skill uses AIPROX_SPEND_TOKEN for paid API access. <br>
Mitigation: Use a limited, revocable spend token and rotate or revoke it if exposure is suspected. <br>


## Reference(s): <br>
- [AIProx homepage](https://aiprox.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sentiment responses can include score, magnitude, emotions, reasoning, confidence, mode, context, and batch summaries.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
