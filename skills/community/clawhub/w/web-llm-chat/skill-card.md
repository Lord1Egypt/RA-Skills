## Description: <br>
Chat with web-based LLMs through the Chrome Relay extension; currently supports Qwen AI for web search, deep research, multi-turn investigations, second opinions, response comparison, and delegated reasoning tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godiao](https://clawhub.ai/user/godiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send prompts to a browser-hosted Qwen Chat session, retrieve responses, and run multi-turn research workflows through a local Chrome Relay setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect and control an attached Qwen browser tab through the local Chrome Relay. <br>
Mitigation: Use a dedicated browser profile and attach only the intended Qwen tab before running the skill. <br>
Risk: The read command can capture visible page text or conversation history from the attached tab. <br>
Mitigation: Avoid using the skill with confidential prompts, private documents, unrelated sensitive tabs, or conversations that should not be copied into agent output. <br>
Risk: Relay access depends on a derived local token from the OpenClaw gateway configuration. <br>
Mitigation: Protect the gateway token, avoid sharing local configuration files, and rotate the token if it may have been exposed. <br>


## Reference(s): <br>
- [Chrome Relay Setup Reference](references/chrome-relay.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/godiao/web-llm-chat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, Markdown, or raw HTML responses, with command-line status and diagnostic output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an attached Chrome Relay session, a Qwen Chat tab, and the ws Node.js package.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
