## Description:

Helps AI-agent users, skill authors, maintainers, and teams turn self-improving and proactive agent workflow needs into practical plans, checklists, artifacts, analysis, or implementation support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to create repeatable workflows for fixing bugs, hardening setup and safety, improving reliability, or creating adjacent self-improving and proactive agent skills. It emphasizes concrete local-friendly outputs such as plans, templates, checklists, analysis, code changes, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad productivity and self-improvement triggers may route unrelated tasks into this workflow helper.

Mitigation: Invoke the skill explicitly by name for intended workflow-help tasks, and disable or ignore implicit activation when it is not relevant.

Risk: Generated workflow advice, code changes, or setup guidance may be incorrect or incomplete for a user's environment.

Mitigation: Review outputs before applying them, validate against the stated success criteria, and scan or test implementation artifacts before deployment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub release page](https://clawhub.ai/kyro-ma/skills/work-productivity-self-improving-workflow-helper-050334)
- [Self-improving agent demand signal](https://clawhub.ai/skills/self-improving-agent)
- [Proactive Agent demand signal](https://clawhub.ai/skills/proactive-agent)
- [Self-Improving + Proactive Agent demand signal](https://clawhub.ai/skills/self-improving)
- [Rate limit feature request signal](https://github.com/Serouce/residualmap-bot/issues/10)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code, shell command, and configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include assumptions, limits, validation notes, and follow-up work when relevant.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
