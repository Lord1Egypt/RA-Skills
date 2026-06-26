## Description: <br>
Helps agents run Chrome on Linux servers in headless or Xvfb-backed headed modes and connect Chrome DevTools MCP for browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodingLink](https://clawhub.ai/user/CodingLink) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to launch Chrome on Linux servers without a GUI, configure Xvfb display settings, and connect Chrome DevTools MCP for scraping, screenshots, debugging, and browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chrome automation on a shared Linux server can expose browser state or DevTools controls if profiles, users, or ports are reused. <br>
Mitigation: Use an isolated container or dedicated host, run Chrome as an unprivileged user, keep DevTools bound to localhost, avoid logged-in personal profiles, and create per-task profile directories. <br>
Risk: Process-kill examples can stop unrelated Chrome or Xvfb sessions on shared systems. <br>
Mitigation: Review killall and pkill commands before use, and scope process management to task-specific ports, displays, or profile directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CodingLink/xvfb-chrome) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with bash command examples and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Chrome launch modes, Xvfb display setup, DevTools MCP connection details, profile directory usage, and screen resolution guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
