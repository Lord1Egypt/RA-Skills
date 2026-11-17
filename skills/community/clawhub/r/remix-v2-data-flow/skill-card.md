## Description:

Guides agents on Remix v2 loaders, actions, deferred data, revalidation logic, pending state, and related migration patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill when implementing or reviewing Remix v2 route data flow, including loaders, actions, streaming with defer/Await, revalidation, and pending UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSRF-related wording could be overread as sufficient protection for cookie-authenticated mutations.

Mitigation: Require explicit server-side CSRF defenses such as token or origin validation, plus normal authorization checks.

Risk: Loader examples can leak sensitive data if copied without projecting server data into safe client-facing DTOs.

Mitigation: Review returned loader and action payloads before use and exclude password hashes, API keys, internal flags, and other sensitive fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/remix-v2-data-flow)
- [Loaders](references/loaders.md)
- [Actions](references/actions.md)
- [Defer & Await](references/defer-await.md)
- [Revalidation & Pending State](references/revalidation.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown guidance with TypeScript and TSX code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable or persistent behavior.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
