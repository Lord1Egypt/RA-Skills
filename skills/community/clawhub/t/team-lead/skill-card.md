## Description:

Multi-Agent Orchestration Lead - Decompose complex tasks, dispatch to specialized agents, aggregate results, and ensure quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linux2010](https://clawhub.ai/user/linux2010)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, researchers, content creators, and team managers use this skill to break complex work into subtasks, coordinate specialized agents, aggregate their outputs, and apply quality checks before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delegate work to spawned or targeted agents and pass user task context to them.

Mitigation: Review delegated task context before execution and avoid sharing secrets, credentials, private documents, or regulated data unless session handling has been reviewed.

Risk: Session logs or exported histories may retain user task content without clear limits.

Mitigation: Confirm OpenClaw logging and history retention behavior before using the skill with sensitive or confidential information.

Risk: The skill is expected to produce Chinese-language prompts and output unless customized.

Mitigation: Customize prompts, templates, and review criteria for the deployment language and require human review of final outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linux2010/skills/team-lead)
- [Publisher profile](https://clawhub.ai/user/linux2010)
- [README.md](README.md)
- [TEST-REPORT.md](TEST-REPORT.md)
- [examples/coding-project.md](examples/coding-project.md)
- [examples/research-workflow.md](examples/research-workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured task plans, JSON configuration examples, code-oriented workflow guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coordinate multiple agent sessions, pass task context to them, aggregate returned content, and produce Chinese-language prompts or output unless customized.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
