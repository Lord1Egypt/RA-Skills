## Description:

Skill Composer orchestrates multiple OpenClaw skills into YAML-defined automation workflows so an agent can run multi-step tasks with one command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to define serial OpenClaw workflows in YAML, preview or validate those workflows, and execute installed skills in sequence for content creation, video processing, and data-reporting pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow files can invoke any installed OpenClaw skill.

Mitigation: Review workflow YAML before execution, run previews first, and restrict callable skills where deployment policy allows.

Risk: Workflow conditions are evaluated as Python code.

Mitigation: Replace condition evaluation with a strict condition parser and fail closed when conditions are invalid.

Risk: Untrusted third-party workflow YAML can trigger unexpected skill execution.

Mitigation: Use workflows from trusted sources only and avoid running external workflow files without review.

Risk: Dependencies are not pinned in the provided install flow.

Mitigation: Pin dependency versions before broad deployment and validate the installation environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/utopiabenben/skills/skill-composer)
- [Project Homepage](https://github.com/utopiabenben/ai-skills)
- [Project Issues](https://github.com/utopiabenben/ai-skills/issues)
- [Portfolio Site](https://utopiabenben.github.io/ai-skills/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text and Markdown with YAML workflow configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workflow execution can create files or directories through the installed skills it invokes.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
