## Description: <br>
A living knowledge base of hard-earned strategy lessons and banned code patterns that helps agents avoid repeating past strategy mistakes by scanning code and generating decision context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tltby12341](https://clawhub.ai/user/tltby12341) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill during iterative strategy development to record lessons, maintain banned code patterns, scan strategy code for known violations, and produce prompt-ready decision context before generating new strategy code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent lesson and ban files can influence future coding decisions with stale, incorrect, sensitive, or prompt-like content. <br>
Mitigation: Review lessons.json and bans.json periodically, avoid storing secrets or untrusted prompt-like text, and remove or correct entries that were recorded in error. <br>
Risk: Using an entry point that is not present in the artifact can lead to failed execution or inconsistent behavior. <br>
Mitigation: Use the included cli.py entry point unless a separate orchestrator module has been verified. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/tltby12341/strategy-constitutional-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local JSON memory files for lessons and banned patterns when used through its Python API or CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
