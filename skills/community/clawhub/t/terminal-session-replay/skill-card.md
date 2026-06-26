## Description: <br>
Record and replay terminal sessions for debugging, documentation, or sharing procedures with teammates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Derick001](https://clawhub.ai/user/Derick001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to record terminal workflows, replay them with timing, manage saved sessions, and export transcripts to markdown for debugging, documentation, or team handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recorded and exported sessions may contain sensitive terminal content such as secrets, API keys, customer data, or private infrastructure output. <br>
Mitigation: Avoid recording sensitive workflows, review and redact transcripts before sharing, and delete or protect ~/.terminal-sessions/ when recordings are no longer needed. <br>
Risk: The tool depends on local terminal recording utilities and is not suitable for unsupported environments. <br>
Mitigation: Use it on Linux or macOS systems with Python 3 and the script command available; use WSL or Cygwin when running from Windows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Derick001/terminal-session-replay) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, JSON command results, and markdown exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records are stored under ~/.terminal-sessions/ as typescript, timing, and metadata files; exported markdown may include captured terminal content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
