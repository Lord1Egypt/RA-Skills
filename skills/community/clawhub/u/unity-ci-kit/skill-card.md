## Description:

Unity CI Kit provides a Python CLI and Unity Editor runner for automated Unity batchmode builds, compile checks, reusable CI pipelines, and structured error parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jssj07](https://clawhub.ai/user/jssj07)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up repeatable CI for Unity projects, run Unity batchmode compilation or builds, and parse results into structured output that agents can use in code-fix workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled runner has unsafe command handling, especially on Windows.

Mitigation: Use the skill only with trusted Unity repositories, review ci_config.json before execution, and prefer argument-list subprocess calls with shell=False before CI use.

Risk: Configurable log and result paths can write outside the intended project area if misconfigured.

Mitigation: Constrain log_file and result_file to project-local paths before running builds in shared or automated environments.

## Reference(s):

- [Unity CI Kit setup guide](references/setup_guide.md)
- [ClawHub Unity CI Kit skill page](https://clawhub.ai/jssj07/skills/unity-ci-kit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, Python code, and C# Unity Editor code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or helps install ci_config.json, ci_result.json, Unity log parsing output, Python CLI commands, and a Unity Editor runner template.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
