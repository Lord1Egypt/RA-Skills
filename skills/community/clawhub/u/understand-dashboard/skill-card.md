## Description:

Launch the interactive web dashboard to visualize a codebase's knowledge graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lum1104](https://clawhub.ai/user/lum1104)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to start a local dashboard for inspecting an existing Understand Anything knowledge graph for a project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install dependencies and execute JavaScript tooling.

Mitigation: Review dependency installation before running, prefer frozen lockfile behavior that fails closed, and use pinned local tooling such as pnpm exec or a pinned Vite binary.

Risk: The skill can start a background local server and open a browser.

Mitigation: Ask before launching the browser or background server, confirm the selected project path, and stop the server when dashboard use is complete.

Risk: Unsafe path handling could affect which directory or graph is used.

Mitigation: Quote paths safely and verify the resolved project directory and knowledge graph path before starting the dashboard.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lum1104/skills/understand-dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts a local Vite dashboard for the selected project when prerequisites are present.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
