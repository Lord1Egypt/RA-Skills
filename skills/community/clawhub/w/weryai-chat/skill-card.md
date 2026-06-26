## Description: <br>
Chat, ask, compare, and inspect WeryAI chat models through the official OpenAI-compatible chat completions API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WeryAI-Developer](https://clawhub.ai/user/WeryAI-Developer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call WeryAI chat completions for general assistant responses, multi-turn message-array conversations, prompt-response tasks, model lookup, and model selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and message arrays selected by the user are sent to WeryAI with WERYAI_API_KEY. <br>
Mitigation: Do not submit secrets or sensitive data unless that matches the user's WeryAI data-handling expectations. <br>
Risk: Real chat completion runs may consume WeryAI credits. <br>
Mitigation: Use dry-run mode to inspect request payloads before making paid API calls. <br>
Risk: An unused balance helper is present in vendored code and may create confusion about account-billing access. <br>
Mitigation: Document or remove the unused helper before deployment if billing-scope clarity is required. <br>


## Reference(s): <br>
- [WeryAI Chat API](references/chat-api.md) <br>
- [Chat Completion API](https://docs.weryai.com/api-reference/chat/chat-completion) <br>
- [Get Chat Models List](https://docs.weryai.com/api-reference/chat/get-chat-models-list) <br>
- [ClawHub Skill Page](https://clawhub.ai/WeryAI-Developer/weryai-chat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON results from Node.js commands, with assistant text, model metadata, dry-run request previews, or structured error messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js >=18 and WERYAI_API_KEY; real chat requests call WeryAI and may consume credits.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
