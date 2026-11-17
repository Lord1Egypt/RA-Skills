## Description:

Use GitHub Spec Kit for Spec-Driven Development. Initialize projects, create specifications, and build software using the /speckit.* slash commands. Supports Claude Code, GitHub Copilot, Gemini CLI, and Codebuddy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aungmyokyaw](https://clawhub.ai/user/aungmyokyaw)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to initialize GitHub Spec Kit projects and guide specification, clarification, planning, and build workflows with supported coding agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to execute mutable remote Git code at run time.

Mitigation: Pin the Git URL to a reviewed commit or release before running initialization.

Risk: Initialization and build workflows may modify project files and Git history.

Mitigation: Run the workflow first in a disposable or isolated repository, inspect generated files, and review Git changes before accepting commits.

Risk: Using --ignore-agent-tools may bypass checks for expected local agent tooling.

Mitigation: Use the flag only after confirming the required tools and reviewing the generated .speckit files and scripts.

## Reference(s):

- [Spec Kit Documentation](https://github.github.com/spec-kit/)
- [GitHub Spec Kit Repository](https://github.com/github/spec-kit)
- [uv Documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline slash commands and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose project files, specifications, plans, generated scripts, and Git changes for user review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
