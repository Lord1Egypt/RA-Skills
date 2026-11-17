## Description:

Chat with web-based LLMs through Chrome Relay, currently supporting Qwen Chat for web search, RAG-style research, multi-turn investigations, and response extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godiao](https://clawhub.ai/user/godiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to delegate search-backed questions, deep research, second-opinion checks, and multi-turn investigations to a web LLM through an attached Chrome Relay session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls an authenticated browser tab through a local Chrome Relay connection and may send prompts or page contents to the wrong place if the wrong tab is attached.

Mitigation: Attach only genuine https://chat.qwen.ai tabs and verify the relay status before sending prompts.

Risk: Sensitive conversation content, secrets, or personal data could be exposed through prompts or read/html output modes.

Mitigation: Avoid sending secrets or personal data to Qwen unless intentional, and avoid read or html output on sensitive conversations.

Risk: Runtime behavior depends on the local Node.js dependency set.

Mitigation: Pin and review dependencies before operational use.

## Reference(s):

- [Chrome Relay Setup Reference](references/chrome-relay.md)
- [ClawHub skill page](https://clawhub.ai/godiao/skills/web-llm-chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text, Markdown, or HTML returned from the web LLM, plus command-line status and troubleshooting output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an attached Chrome Relay tab; read and HTML output modes can expose current page content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
