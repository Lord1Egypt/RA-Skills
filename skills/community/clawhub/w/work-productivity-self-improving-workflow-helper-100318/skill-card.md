## Description:

Helps AI-agent users, skill authors, maintainers, and teams turn self-improving workflow needs into practical plans, checklists, artifacts, analyses, code changes, and validation notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to structure self-improving agent workflow work such as bug fixing, setup hardening, reliability improvements, adjacent skill creation, and repeatable local-friendly execution plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may cause the skill to run on loosely related productivity, improvement, or logging requests.

Mitigation: Prefer explicit invocation by skill name and confirm that the user's request is about agent reliability, bug fixing, setup hardening, or self-improving workflow planning before applying the workflow.

Risk: Generated plans, checklists, code changes, or commands may be incomplete or context-dependent.

Mitigation: Validate outputs against the user's stated success criteria and review proposed changes or commands before using them in a live environment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Demand: self-improving-agent](https://clawhub.ai/skills/self-improving-agent)
- [ClawHub Skill Demand: self-improving](https://clawhub.ai/skills/self-improving)
- [GitHub Issue Demand Signal](https://github.com/pauljsnider/allplays/issues/3455)
- [OpenClaw Skill Article Demand Signal](https://segmentfault.com/a/1190000047666647)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, remaining risks, and follow-up work.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
