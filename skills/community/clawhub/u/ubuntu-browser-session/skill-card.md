## Description: <br>
Use when a request needs a real Ubuntu Server browser session with durable site login reuse, bounded manual login recovery, or host-side page inspection for protected sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LINSUISHENG034](https://clawhub.ai/user/LINSUISHENG034) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to open and inspect protected sites in a real Ubuntu Server browser, reuse durable logged-in site sessions, and recover expired or challenged sessions with bounded manual help. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: noVNC access can expose a logged-in browser session to anyone who can reach the service. <br>
Mitigation: Prefer SSH tunnels or localhost-only exposure, firewall the noVNC port, and stop the assisted overlay after login recovery. <br>
Risk: Durable browser profiles and session metadata can retain access to protected sites after a task finishes. <br>
Mitigation: Install only on hosts and networks you control, periodically review stored profiles and session metadata under ~/.agent-browser, and remove profiles that are no longer needed. <br>
Risk: The skill can act through authenticated browser sessions, so wrong account selection could affect protected resources. <br>
Mitigation: Use the documented default site identity model and require an explicit session-key before using any non-default identity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LINSUISHENG034/ubuntu-browser-session) <br>
- [Use Cases](references/use-cases.md) <br>
- [Assisted Session Flow](references/assisted-session-flow.md) <br>
- [Session Storage](references/session-manifest.md) <br>
- [Manual Fallback](references/manual-fallback.md) <br>
- [Forum/Search Result Enhancements](references/forum-enhancements.md) <br>
- [Validation Findings](references/validation-findings.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit noVNC URLs, CDP page snapshots, session manifest updates, and browser profile state under ~/.agent-browser.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
