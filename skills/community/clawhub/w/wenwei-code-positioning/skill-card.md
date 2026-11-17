## Description:

Helps an agent locate the key implementation code for a described requirement or issue by tracing from a specified code entry point through components, calls, interfaces, and routes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wed840313](https://clawhub.ai/user/wed840313)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to answer where a specific behavior, bug, API path, UI element, or business rule is implemented in a codebase. It is intended for focused code-navigation tasks that produce a concise conclusion, short call chain, and relevant code excerpts with paths and line numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may summarize or quote source code from the current workspace back into chat.

Mitigation: Use it only on repositories where sharing relevant implementation snippets in the agent conversation is acceptable.

Risk: Vague requests or missing entry points can lead to incomplete or incorrect code-location conclusions.

Mitigation: Provide a concrete problem, behavior, API path, UI text, or field name together with a specific entry file or symbol.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown with code excerpts, file paths, line numbers, and concise call-chain notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are expected to be grounded in files available in the current workspace and to stop when the key implementation location is found.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
