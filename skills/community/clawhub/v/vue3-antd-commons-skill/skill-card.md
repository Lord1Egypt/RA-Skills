## Description:

Chinese-language Vue 3, Ant Design Vue, TypeScript, Vue Router, Pinia, Vite, fetch, and publish-commons reference material for frontend development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li-4568](https://clawhub.ai/user/li-4568)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill as a Vue 3 and Ant Design Vue reference for component patterns, TypeScript typing, routing, Pinia state management, Vite configuration, fetch wrappers, and publish-commons integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example networking code and token-handling patterns may be copied into production without application-specific hardening.

Mitigation: Validate API origins, avoid sending bearer tokens to caller-controlled URLs, and prefer safer session handling than persistent localStorage for sensitive tokens.

Risk: The publish-commons dependency is shown as a normal install step without release pinning guidance in the artifact.

Mitigation: Pin and review the publish-commons dependency version before using it in a production project.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/li-4568/skills/vue3-antd-commons-skill)
- [Artifact README](artifact/README.md)
- [Fetch wrapper example](artifact/examples/fetch-wrapper.md)
- [Prop type definition example](artifact/examples/prop-type-definition.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, Vue, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Chinese-language frontend reference material and example snippets; artifact docs describe optional Markdown, HTML, and PDF documentation outputs.]

## Skill Version(s):

1.0.1 (source: server evidence and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
