## Description: <br>
Mirror your Claude Code terminal in a browser for remote viewing and real-time interaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[topcheer](https://clawhub.ai/user/topcheer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to expose a Claude Code terminal session through a browser for remote viewing or real-time interaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally creates a public interactive terminal session that can expose credentials, private files, or privileged shell access. <br>
Mitigation: Install only when public terminal sharing is intended, treat the generated URL like a password, use non-sensitive directories, and avoid privileged shells. <br>
Risk: Terminal output is cached, so new viewers may see prior session history. <br>
Mitigation: Avoid sharing sessions containing secrets or private output, and stop the session immediately when finished. <br>
Risk: The security evidence reports weak activation wording and limited safeguards around the public session. <br>
Mitigation: Confirm the user explicitly requested remote terminal sharing before running the commands. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/topcheer/remoting) <br>
- [Project homepage](https://github.com/topcheer/claude-remoting) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require Node.js and may create a public interactive terminal session.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
