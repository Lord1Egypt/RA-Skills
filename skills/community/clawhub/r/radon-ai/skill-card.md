## Description:

Use Radon IDE's AI tools for React Native development to query library docs, view logs and network traffic, take screenshots, inspect component trees, and interact with the user's app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[latekvo](https://clawhub.ai/user/latekvo)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill while working on React Native or Expo projects with Radon IDE running in VS Code or Cursor. It helps agents retrieve React Native library documentation, inspect app runtime state, review logs and network traffic, capture screenshots, and reload the app during debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: App logs, screenshots, component hierarchy, and network request details can expose sensitive visible content, headers, bodies, cookies, tokens, or account data to the agent context.

Mitigation: Use the skill with development or test data unless the project owner is comfortable sharing that information with the agent; review captured data before acting on or redistributing it.

Risk: Documentation and debugging responses augmented by the skill can still contain LLM errors or incomplete library context.

Mitigation: Verify important implementation decisions against authoritative project behavior, source documentation, tests, and reviewer judgment before applying changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tool-derived text, snippets, and actionable guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include information derived from app logs, screenshots, component trees, library documentation, and network request details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
