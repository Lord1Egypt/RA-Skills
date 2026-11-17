## Description:

Task Director turns complex tasks into movie storyboards so an agent can create a plan, review it, and execute it step by step with fallback support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[besty0121](https://clawhub.ai/user/besty0121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to break complex operational tasks into reviewable scenes and shots, approve the plan, then execute each step while tracking status, outputs, skipped steps, and fallback paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or edited scene commands may install packages, remove files, or make network calls when an agent executes them.

Mitigation: Review every scene and shot before approval, especially command fields and fallbacks, and execute only commands appropriate for the workspace.

Risk: Untrusted movie IDs may allow the CLI to read or overwrite JSON files outside the intended movie storage directory.

Mitigation: Use trusted movie IDs only until path validation is fixed, and prefer a version that confines all reads and writes to ~/.openclaw/memory/movies/.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/besty0121/skills/task-director)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON task plans and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI stores task-plan JSON files under ~/.openclaw/memory/movies/ and returns the next executable shot as JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
