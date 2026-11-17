## Description:

Helps agent users, skill authors, maintainers, and teams turn Proactive Agent-style workflow needs into practical plans, checklists, artifacts, analyses, code changes, and validation notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to adapt popular Proactive Agent-style patterns into reliable local workflows. It supports practical planning, bug fixing, setup hardening, safety review, implementation support, and reusable decision aids.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate too broadly for generic productivity requests because implicit invocation is enabled and trigger wording is broad.

Mitigation: Use explicit invocation or narrow the trigger terms before deployment in environments that require precise routing.

Risk: Workflow, code, or setup guidance may be incomplete or unsuitable for a user's specific environment.

Mitigation: Review generated artifacts against the stated success criteria, scan code before use, and keep assumptions and required inputs visible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-proactive-agent-workflow-helper-041220)
- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub Skill Demand: Proactive Agent](https://clawhub.ai/skills/proactive-agent)
- [Popular ClawHub Skill Demand: Self-Improving + Proactive Agent](https://clawhub.ai/skills/self-improving)
- [Popular ClawHub Skill Demand: ontology](https://clawhub.ai/skills/ontology)
- [AI Project Management Topics](https://blog.csdn.net/weixin_51988935/article/details/163121882?ops_request_misc=elastic_search_misc&request_id=3c5e38ef05bd4ab69b6abf25a0d539f7&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~ElasticSearch~search_v2-4-163121882-null-null.142^v102^pc_search_result_base1&utm_term=proactive-agent%20proactive%20transform%20task)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored to the user's stated outcome and include assumptions, validation notes, and remaining risks when helpful.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
