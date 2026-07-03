## Description: <br>
Create and send native Slack Block Kit messages, including tables, code cards, structured layouts, buttons, inputs, and rich Slack blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bill492](https://clawhub.ai/user/bill492) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to draft portable rich Slack messages or native Block Kit payloads, validate local samples, and prepare Slack API posts with accessibility fallbacks and token handling guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Slack messages or interactive workflows may be posted to live channels before review. <br>
Mitigation: Review generated payloads and require explicit confirmation before live posts, buttons, inputs, or other interactive workflows. <br>
Risk: Slack bot tokens could be exposed while composing or debugging API calls. <br>
Mitigation: Resolve tokens from configured secrets or environment variables, and do not place token values in prompts, generated messages, or logs. <br>


## Reference(s): <br>
- [Slack Block Kit Reference](https://api.slack.com/block-kit/reference) <br>
- [Slack chat.postMessage API](https://slack.com/api/chat.postMessage) <br>
- [Slack Agent Blocks](https://api.slack.com/partners/thinking-steps) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Slack Block Kit JSON payloads, Slack API examples, and sample validation commands.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
