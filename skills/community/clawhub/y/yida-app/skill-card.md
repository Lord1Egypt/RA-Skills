## Description:

Yida App guides agents through building a complete Yida application from scratch, including app creation, requirements analysis, page and form creation, code writing, and deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicky1108](https://clawhub.ai/user/nicky1108)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and application builders use this skill to plan and create Yida applications from scratch. It supports the full workflow from requirement documentation through custom page code, form setup, and publication to a Yida app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install unaudited dependencies while preparing the Yida publishing workflow.

Mitigation: Review dependency installation steps before execution and avoid running them in production projects until dependencies are verified.

Risk: The skill can publish changes to a live Yida application using a stored login session.

Mitigation: Require explicit confirmation before publishing, verify target app identifiers and organization corpId, and use non-production apps until the target is confirmed.

Risk: The skill depends on Yida login cookies that can create or modify applications.

Mitigation: Use only trusted login sessions, clear stale cookies when switching accounts, and limit agent access to the intended Yida organization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicky1108/skills/yida-app)
- [Yida application platform](https://ding.aliwork.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce PRD documentation, page source code, form schema references, cache configuration guidance, and publication steps for Yida applications.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
