## Description:

Enables agents to self-monitor execution, reflect on tasks, analyze errors, and adjust learning strategies through metacognitive processes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add local self-monitoring, execution reflection, error analysis, and learning-progress summaries to agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitored contexts, decisions, events, reflections, and raw error messages may contain sensitive task data while held in process memory.

Mitigation: Sanitize or omit secrets before passing context and error objects into monitoring or reflection calls.

Risk: The package documentation and code comments are primarily Chinese-language, which may slow review for teams that do not read Chinese.

Mitigation: Have a qualified reviewer inspect the package behavior and translated documentation before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-agent-metacognition)
- [Publisher profile](https://clawhub.ai/user/yuyonghao-123)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [JavaScript API results and JSON-like report objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains execution sessions, decisions, reflections, lessons, patterns, recommendations, and learning statistics in process memory.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
