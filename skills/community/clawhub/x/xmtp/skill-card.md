## Description: <br>
Make an OpenClaw agent messageable on XMTP so humans and other agents can reach it by address for ongoing two-way conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saulmc](https://clawhub.ai/user/saulmc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up an OpenClaw agent as a persistent XMTP endpoint for agent-to-agent or human-to-agent messaging. It is intended for bridge setup, owner/public message routing, and deployment guidance rather than one-off message sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a persistent XMTP-facing agent endpoint that can receive messages from public users. <br>
Mitigation: Install it only when a persistent messaging endpoint is intended, require explicit setup confirmation, and keep owner/public routing configured before starting the bridge. <br>
Risk: XMTP credentials and wallet material are stored in ~/.xmtp/.env. <br>
Mitigation: Use a fresh no-funds wallet, protect the environment file with restrictive permissions, and avoid committing it to version control. <br>
Risk: Prompt-only public restrictions may not reliably limit tool access. <br>
Mitigation: Run separate low-privilege tool profiles for public users and avoid relying on public-prompt.md as the only access boundary. <br>
Risk: A long-running bridge can broaden the impact of misconfiguration. <br>
Mitigation: Run the bridge under a dedicated user or container and avoid running it as root. <br>


## Reference(s): <br>
- [ClawHub XMTP Skill Page](https://clawhub.ai/saulmc/xmtp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup commands, bridge script examples, access-control guidance, and operational notes.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
