## Description:

Helps AI-agent users, skill authors, maintainers, and teams create practical workflows, artifacts, checklists, analyses, and implementation support for self-improving and proactive agent-style productivity work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to turn self-improving or proactive-agent productivity requests into concrete plans, checklists, code changes, configuration guidance, and validation notes while keeping execution local-hardware friendly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad productivity and bug-fix trigger language may cause the skill to activate when a more specific workflow would be better.

Mitigation: Invoke the skill by exact name for intended use and narrow implicit-routing triggers where the runtime allows it.

Risk: The skill can produce workflow, checklist, code, shell-command, or configuration guidance that may be incomplete or unsuitable for a specific environment.

Mitigation: Review outputs against the stated success criteria before applying changes, and run normal tests, scans, or command dry-runs before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-self-improving-workflow-helper-130329)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub skill demand: self-improving agent](https://clawhub.ai/skills/self-improving-agent)
- [Popular ClawHub skill demand: Proactive Agent](https://clawhub.ai/skills/proactive-agent)
- [Popular ClawHub skill demand: Self-Improving + Proactive Agent](https://clawhub.ai/skills/self-improving)
- [OpenClaw Skills article](https://segmentfault.com/a/1190000047666647)
- [Self-improving Agent category](https://blog.csdn.net/qq_42540492/category_13024655.html?ops_request_misc=elastic_search_misc&request_id=32d2c3ae1ff64c49b030ee356dc3059f&biz_id=&utm_medium=distribute.pc_search_result.none-task-special_column-2~all~ElasticSearch~search_v2-1-13024655-null-null.142^v102^pc_search_result_base9&utm_term=self-improving-proactive-agent%20self%20improving%20proactive)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code, configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reusable checklists, workflow templates, assumptions, validation notes, and follow-up risks.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
