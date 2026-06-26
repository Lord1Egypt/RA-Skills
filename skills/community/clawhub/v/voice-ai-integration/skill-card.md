## Description: <br>
Integrate Shengwang products, including ConvoAI voice agents, RTC audio/video, RTM messaging, Cloud Recording, and token generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hugochaan](https://clawhub.ai/user/hugochaan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and implement Shengwang voice, video, messaging, recording, token, and ConvoAI integrations. It routes requests to the relevant product module and provides reference-backed implementation, debugging, and configuration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may fetch Shengwang documentation or inspect sample repositories during normal use. <br>
Mitigation: State what will be downloaded before network fetches or repository inspection, use trusted Shengwang documentation and listed sample repositories, and avoid sending user project context with documentation fetches. <br>
Risk: Voice, video, recording, transcript, and conversation-history workflows can involve sensitive personal or business data. <br>
Mitigation: Confirm legal consent, retention, and data-handling requirements before enabling recording, transcript, or history features. <br>
Risk: Credential handling mistakes can expose App IDs, customer secrets, app certificates, RTC tokens, or provider keys. <br>
Mitigation: Use environment variables or a secret manager, keep production secrets out of client code and logs, and use placeholders in generated examples. <br>
Risk: LLM or MCP endpoints connected to voice agents may introduce unintended tool access or data exposure. <br>
Mitigation: Connect only trusted LLM or MCP endpoints and configure explicit tool allowlists. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hugochaan/voice-ai-integration) <br>
- [Shengwang documentation](https://doc.shengwang.cn/) <br>
- [Shengwang console](https://console.shengwang.cn/) <br>
- [Shengwang Community GitHub](https://github.com/Shengwang-Community) <br>
- [Credentials and authentication](references/general/credentials-and-auth.md) <br>
- [ConvoAI voice agents](references/conversational-ai/README.md) <br>
- [RTC audio/video](references/rtc/README.md) <br>
- [RTM messaging](references/rtm/README.md) <br>
- [Cloud Recording](references/cloud-recording/README.md) <br>
- [Token server](references/token-server/README.md) <br>
- [Doc fetching guide](references/doc-fetching.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Shengwang API request examples, environment variable guidance, routing recommendations, and implementation steps.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
