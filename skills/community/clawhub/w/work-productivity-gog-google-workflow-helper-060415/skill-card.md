## Description:

Helps agents create practical Gog-style Google Workspace workflows, checklists, analyses, code changes, and setup-hardening guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to adapt Gog-style Google Workspace productivity workflows, fix bugs, harden setup and safety, improve reliability, or create adjacent skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation and productivity keywords may activate the skill for loosely related Gog or Google Workspace requests.

Mitigation: Narrow triggers where possible and confirm user intent before applying the workflow to sensitive or unrelated tasks.

Risk: Users may provide unnecessary private Gmail, Calendar, Drive, or Contacts data while seeking workflow help.

Mitigation: Ask only for task-relevant details, avoid collecting private content unless required, and redact sensitive values before using examples or artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-gog-google-workflow-helper-060415)
- [Requirement Plan](references/requirement-plan.md)
- [Gog demand signal](https://clawhub.ai/skills/gog)
- [GitHub issue demand signal](https://github.com/open-telemetry/opentelemetry-go-compile-instrumentation/issues/708)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code, shell command, checklist, template, analysis, or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task-specific artifacts with assumptions, validation notes, and remaining risks when helpful]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
