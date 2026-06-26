## Description: <br>
Generates concise WeChat Moments marketing copy for microbusinesses, ecommerce, and local stores using DeepSeek. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duoduoks](https://clawhub.ai/user/duoduoks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Small business owners, ecommerce operators, marketers, and agents use this skill to draft short WeChat Moments promotional posts in styles such as promotion, recommendation, emotional storytelling, educational tips, and interaction prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends product and campaign prompts to DeepSeek for generation. <br>
Mitigation: Do not provide confidential customer data, unreleased campaign plans, or sensitive business details unless approved for DeepSeek processing. <br>
Risk: The skill requires a DeepSeek API key and may consume paid API quota. <br>
Mitigation: Use a key with appropriate billing limits and store it through environment or OpenClaw configuration with normal secret handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duoduoks/wechat-copywriter) <br>
- [DeepSeek API endpoint used by artifact](https://api.deepseek.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text marketing copy, with usage examples shown in Markdown and CLI output printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated copy is short-form marketing text, typically 50-150 Chinese characters, and depends on a DeepSeek API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
