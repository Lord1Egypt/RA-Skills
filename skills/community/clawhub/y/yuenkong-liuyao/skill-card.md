## Description: <br>
玄空数术·六爻占卜 supports divination readings and follow-up chat, using user-provided numbers, question context, and a provider API key to call the Yao Liuyao service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigbigtooth](https://clawhub.ai/user/bigbigtooth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to request Liuyao divination readings, select an appropriate divination category, and ask follow-up questions about the generated reading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a chat-supplied provider API key in ~/.liuyao_key. <br>
Mitigation: Use a dedicated revocable key, delete ~/.liuyao_key when finished, and prefer platform-managed secrets before deployment. <br>
Risk: The skill instructs the agent to run shell commands that include raw user text. <br>
Mitigation: Review command arguments before execution and revise the skill to use safe argument passing for user-supplied questions. <br>
Risk: Divination questions and provider API keys are sent to yao.gizzap.com. <br>
Mitigation: Avoid sensitive personal, health, financial, or account details and install only when this data sharing is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/bigbigtooth/yuenkong-liuyao) <br>
- [Yao Liuyao service endpoint](https://yao.gizzap.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and service JSON responses interpreted for the user] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a separate downloaded divination image followed by text when the service returns an image URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
