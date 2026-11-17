## Description:

Complete Spec-Driven Development (SDD) orchestrator for OpenClaw. Initializes SpecKit and manages the full engineering lifecycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinayakv22](https://clawhub.ai/user/vinayakv22)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to guide an OpenClaw agent through a Spec-Driven Development workflow, from project constitution and requirements specification through planning, task breakdown, consistency analysis, and implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled shell scripts contain a command-execution flaw that can be influenced by untrusted branch, environment, or project state.

Mitigation: Review or patch the shell scripts before use, especially common.sh, and run the workflow only in trusted repositories and environments.

Risk: The workflow can modify repository files and may commit, push, or create branches when enabled.

Mitigation: Enable automated git operations only after explicit user approval and confirm repository write access and target branch expectations before running the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vinayakv22/skills/speckit-workflow)
- [github/spec-kit](https://github.com/github/spec-kit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown workflow guidance with shell command snippets, repository files, and generated specification artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project files and, when explicitly enabled by the user, perform git branch, commit, and push operations.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
