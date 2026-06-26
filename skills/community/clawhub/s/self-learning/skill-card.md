## Description: <br>
Self Learning Skill analyzes agent conversations to extract durable memory, corrections, errors, and feature requests, then updates workspace memory and learning files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Acczdy](https://clawhub.ai/user/Acczdy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain agent memory, capture user corrections and errors, and keep workspace guidance files current through reviewable updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can analyze conversation history and persist information into agent memory files. <br>
Mitigation: Use it only in workspaces where conversation history and memory files are safe to analyze and persist, and avoid storing secrets or personal data in agent memory. <br>
Risk: Automated memory updates can change persistent guidance or learning records in ways that affect future agent behavior. <br>
Mitigation: Run with --dry-run first, inspect the proposed diffs manually, and prefer an explicit --workspace path. <br>
Risk: The server security review flags weak review controls around broad file and conversation access. <br>
Mitigation: Review carefully before installing and keep confirmation controls enabled for destructive changes. <br>


## Reference(s): <br>
- [Self Learning Skill on ClawHub](https://clawhub.ai/Acczdy/self-learning) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [OpenClaw Hook Configuration](artifact/hooks/openclaw/HOOK.md) <br>
- [Default Configuration](artifact/config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, YAML configuration, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update persistent memory and learning files in the selected workspace.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
