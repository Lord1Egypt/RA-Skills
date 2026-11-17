## Description:

Universal AI Interface framework for making applications AI-controllable. Use when adding AI tool decorators, setting up chat adapters, creating AI-callable functions, or integrating CopilotKit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianderrington](https://clawhub.ai/user/ianderrington)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to integrate the Supernal Interface framework, expose typed app functions to AI assistants, configure chat adapters, bind React state, and set up testing utilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned @supernal/interface package version may introduce unreviewed dependency changes.

Mitigation: Pin @supernal/interface to a reviewed version and use a lockfile before deployment.

Risk: Exposing app functions or readable state to AI assistants can allow mutation of data or access to sensitive user context.

Mitigation: Review and limit the functions and state exposed to assistants, especially capabilities that mutate data or read sensitive context.

## Reference(s):

- [Supernal Interface on ClawHub](https://clawhub.ai/ianderrington/skills/supernal-interface)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes installation, decorators, adapters, React hooks, storage adapters, and testing utilities.]

## Skill Version(s):

1.0.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
