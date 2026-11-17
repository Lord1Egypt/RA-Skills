## Description:

Persistent memory for repeated browser work that helps an agent load a few relevant notes before revisiting sites or flows and save durable site knowledge after the task finishes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[littleyier](https://clawhub.ai/user/littleyier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and browser-using agents use this skill to recall reusable site notes before repeated browser tasks and save durable selectors, routes, preferences, and warnings afterward.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent cross-project browser memory can carry sensitive, personal, stale, or site-specific information into later tasks.

Mitigation: Use a project-scoped SITE_MEMORY_HOME or another low-sensitivity memory root, review recalled notes before use, and avoid storing secrets, personal data, session state, or copied webpage instructions.

Risk: The bundled browser helper can read and change pages in a live, logged-in Chrome session when remote debugging is enabled.

Mitigation: Use a separate low-sensitivity browser profile, enable remote debugging only for intended sessions, and confirm sensitive or irreversible browser actions before executing them.

Risk: Remembered selectors, routes, button labels, and page behavior can become stale as websites change.

Mitigation: Treat stored notes as leads and re-check selectors, URLs, and flows against the live page before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/littleyier/skills/site-memory)
- [Bundled Chrome CDP README](artifact/vendor/chrome-cdp-skill/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON command outputs and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include recall and distillation prompts; selected note reads are scoped to the configured memory root.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
