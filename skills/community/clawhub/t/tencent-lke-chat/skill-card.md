## Description: <br>
Guides agents in calling Tencent Cloud LKE's HTTP SSE chat API, including sending messages and parsing streaming reply, token_stat, reference, error, and thought events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijiayi980130](https://clawhub.ai/user/lijiayi980130) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to integrate an agent with Tencent Cloud LKE chat over HTTP SSE, configure request fields, and handle streaming response events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, visitor IDs, custom variables, labels, file URLs, and thought or raw output may contain sensitive data that is sent to or received from Tencent Cloud. <br>
Mitigation: Use the skill only for approved Tencent Cloud LKE workflows, minimize sensitive inputs, and avoid regulated personal data unless the deployment has explicit approval. <br>
Risk: Passing the AppKey directly on the command line can expose the key through shell history, process listings, or logs. <br>
Mitigation: Use a dedicated AppKey, prefer environment variables or a secret manager, restrict access, and rotate the key if exposure is suspected. <br>
Risk: Raw SSE output, references, and thought/debugging events can disclose service responses or internal reasoning-like content to logs or downstream users. <br>
Mitigation: Filter or redact raw output before logging or display, and review thought/debugging content before sharing it outside the intended workflow. <br>


## Reference(s): <br>
- [HTTP SSE API Reference](artifact/references/api_reference.md) <br>
- [Example SSE Chat Client](artifact/scripts/sse_chat.py) <br>
- [Tencent Cloud LKE SSE Endpoint](https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse) <br>
- [ClawHub Skill Page](https://clawhub.ai/lijiayi980130/tencent-lke-chat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples, shell commands, and Python code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request fields, SSE event parsing guidance, model options, error-code explanations, and client execution examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
