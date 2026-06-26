## Description: <br>
Create and reuse a secure shared terminal handoff when a human must authenticate first and the agent must resume work in the same shell session afterward. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonathan97480](https://clawhub.ai/user/jonathan97480) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to coordinate human-authenticated SSH, sudo, or temporary browser-terminal handoffs so an agent can continue in the same tmux-backed shell session without receiving secrets in chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose high-impact writable shell access through temporary local or LAN terminal endpoints. <br>
Mitigation: Install only when human-auth-first terminal sharing is needed; prefer plain tmux or localhost-only mode, and avoid public tunnels or public reverse proxies. <br>
Risk: One-shot URLs, tokens, and browser sessions can grant shell access if shared with the wrong party before expiry. <br>
Mitigation: Treat printed URLs and tokens as shell credentials, use short TTLs, and restrict LAN access to a single trusted client IP. <br>
Risk: Temporary ttyd or proxy processes and tmux sessions may remain available after the handoff if cleanup is missed. <br>
Mitigation: Run the provided cleanup command, verify ttyd and proxy processes have stopped, and review whether the tmux session should remain active. <br>


## Reference(s): <br>
- [SSH Handoff ClawHub page](https://clawhub.ai/jonathan97480/ssh-handoff) <br>
- [Secure web-terminal design notes](references/design-notes.md) <br>
- [SSH handoff examples](references/examples.md) <br>
- [LAN-restricted browser terminal pattern](references/lan-restricted.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose temporary tmux, ttyd, Node proxy, firewall, and cleanup commands; does not produce persistent application data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
