## Description:

Creates a Vue 3 + TypeScript data-dashboard scaffold with Vite, ECharts, Axios, Pinia, Element Plus, vue3-digital-flop, sample JSON data, and verification guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyumingben](https://clawhub.ai/user/liyumingben)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to initialize and customize Vue 3 data-visualization dashboard projects. It is intended for data-screen scaffolding, JSON-backed dashboard pages, and adding ECharts-based chart modules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Frontend dependencies may become outdated or unsuitable for production use with untrusted data.

Mitigation: Review and update npm dependencies, especially ECharts and plugins, before production deployment.

Risk: The lockfile resolves packages through registry.npmmirror.com, which may not match an organization's package-source policy.

Mitigation: Change the npm registry or regenerate the lockfile under the target organization's approved registry policy.

Risk: Untrusted chart labels or HTML-capable chart content could be rendered without sufficient sanitization.

Mitigation: Sanitize or validate external data before passing it into chart options or UI components.

Risk: The Vite development server could be reachable beyond the intended local environment if host binding is changed or left ambiguous.

Mitigation: Set Vite host binding explicitly when the development server should not be reachable on the local network.

Risk: The scaffold includes Chinese locale assumptions and demonstration data.

Mitigation: Document or adapt the locale and replace sample JSON with reviewed production data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liyumingben/skills/vue-bigscreen-scaffold)
- [Vue3 dashboard scaffold README](artifact/assets/vue-bigscreen-scaffold/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with file paths, shell commands, and Vue/TypeScript scaffold files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a Vue 3 scaffold template, sample JSON data files, npm scripts, and a scaffold verification script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
