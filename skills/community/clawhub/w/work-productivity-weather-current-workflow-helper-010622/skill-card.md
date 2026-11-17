## Description:

Helps agent users and skill authors plan, debug, harden, and validate Weather-style workflow skills with reusable checklists, implementation support, and verification notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, agent users, maintainers, and skill authors use this skill to turn demand for Weather-style workflows into practical plans, fixes, setup hardening steps, reliability improvements, adjacent skill ideas, and validation checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may cause the skill to trigger on generic weather, API key, or productivity requests where a narrower skill would be better.

Mitigation: Review and narrow trigger keywords or disable implicit invocation when precise routing matters.

Risk: Workflow guidance may produce plans or code suggestions that do not fit the user's actual weather API, deployment environment, or safety requirements.

Mitigation: Validate assumptions, check generated artifacts against stated success criteria, and review code or configuration before use.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-weather-current-workflow-helper-010622)
- [Weather Skill Demand Signal](https://clawhub.ai/skills/weather)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include visible assumptions, success criteria, validation notes, and remaining risks when relevant.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
