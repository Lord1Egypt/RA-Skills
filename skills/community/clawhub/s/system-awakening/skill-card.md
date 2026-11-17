## Description:

System Awakening designs structured learning skill trees, curates YouTube, Bilibili, and Google resources, generates local talent Skill files, and supports learning and execution modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrxparley](https://clawhub.ai/user/zrxparley)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a learning goal into a staged skill tree with curated resources, practice tasks, progress tracking, and optional task execution based on learned skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent local Skill files and progress records.

Mitigation: Inspect every generated SKILL.md before allowing it to persist, load, or run, and remove generated progress records when they are no longer needed.

Risk: The skill relies on web searches for learning roadmaps and resource links, which can produce outdated, low-quality, or untrusted materials.

Mitigation: Review curated links before using them and prefer official documentation or well-maintained sources.

Risk: Execution-mode tasks may perform broad actions using learned skill capabilities.

Mitigation: Require explicit confirmation before any execution-mode task touches files, credentials, servers, external services, or agent workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zrxparley/skills/system-awakening)
- [Nuwa Skill](https://github.com/alchaincyf/nuwa-skill)
- [Creator profile](https://x.com/AlchainHust)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with resource links, code snippets, progress tables, and generated Skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent local Skill files and progress records when the agent environment permits file writes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
