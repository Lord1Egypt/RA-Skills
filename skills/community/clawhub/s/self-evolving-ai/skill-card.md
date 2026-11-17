## Description: <br>
自我进化AI helps coding agents capture lessons, errors, and feature requests into persistent project memory, track recurring patterns, and promote repeated learnings into project instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to maintain structured project memory for corrections, errors, feature requests, recurring patterns, and reusable lessons. It is intended for long-running agent projects and teams that want repeated operational knowledge promoted into files such as AGENTS.md, CLAUDE.md, or Copilot instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can capture conversations, command output, secrets, personal details, or business-sensitive project context. <br>
Mitigation: Require explicit confirmation before every write, redact sensitive details from prompts and errors, and keep .learnings local unless intentionally shared. <br>
Risk: Promoting repeated patterns into AGENTS.md, CLAUDE.md, or Copilot instruction files can change future agent behavior across the project. <br>
Mitigation: Review diffs before instruction-file changes and only promote concise, validated rules that are broadly applicable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/self-evolving-ai) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file templates, decision tables, and fenced shell or JSON snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .learnings Markdown files and propose changes to project instruction files; review all writes before applying them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
