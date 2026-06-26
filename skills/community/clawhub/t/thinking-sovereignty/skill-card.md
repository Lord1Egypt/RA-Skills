## Description: <br>
Thinking Sovereignty helps agents apply an independent reasoning framework and maintain traceable local memory practices for autonomous cognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwinjhlee](https://clawhub.ai/user/edwinjhlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to establish an agent reasoning posture centered on understanding, verification, deliberate pacing, and local traceability. It is intended for sessions where the agent should pause to reason, ask for clarification, or maintain project memory with user oversight. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents toward persistent local memory logs, which may capture secrets, private prompts, credentials, or sensitive project data. <br>
Mitigation: Require explicit approval before log writes, restrict storage to a known directory, and exclude secrets and sensitive data from memory logs. <br>
Risk: The skill encourages backup, git status or submodule inspection, and commit decisions with limited user control. <br>
Mitigation: Require explicit approval before backups, git inspections, or commits, and review diffs before any repository change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edwinjhlee/thinking-sovereignty) <br>
- [Repository listed in metadata](https://github.com/x-cmd-skill/thinking-sovereignty) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with example workflows, directory structure, and inline shell-oriented actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Markdown-only skill; no detected API keys, MCP tools, or runtime dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
