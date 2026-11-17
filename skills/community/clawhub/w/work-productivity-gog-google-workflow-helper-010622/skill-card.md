## Description:

Helps AI-agent users, skill authors, maintainers, and teams create practical Gog-style workflows for bug fixing, setup hardening, reliability improvement, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Gog-style productivity, Google Workspace, CLI, and workflow-fix requests into concise plans, checklists, artifacts, analysis, or implementation support. It is intended for practical local-hardware-friendly work that surfaces assumptions, success criteria, validation notes, and follow-up risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation terms may activate the skill for general Google Workspace, CLI, Gmail, Drive, Contacts, or bug-fix requests.

Mitigation: Invoke the skill explicitly for Gog-style workflow planning, and review whether the generated plan is appropriate before using it for sensitive workspace tasks.

Risk: Workflow proposals may provide incomplete or misleading guidance if the user's constraints, available inputs, or success criteria are unclear.

Mitigation: Restate assumptions, ask only for materially missing information, and validate the final artifact against the stated success criteria before acting on it.

## Reference(s):

- [Requirement Plan](artifact/references/requirement-plan.md)
- [Work Productivity Gog Google Workflow Helper on ClawHub](https://clawhub.ai/kyro-ma/skills/work-productivity-gog-google-workflow-helper-010622)
- [Popular ClawHub skill demand: Gog](https://clawhub.ai/skills/gog)
- [Tell HN: Forget selectors and screenshots. The agentic web lives in your shell](https://news.ycombinator.com/item?id=48540019)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only workflow helper; no executable code or persistence is bundled.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
