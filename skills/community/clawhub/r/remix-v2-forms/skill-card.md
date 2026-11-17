## Description:

Guides agents in implementing Remix v2 form submissions, fetcher-based mutations, pending state, optimistic UI, intent actions, and file uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when building Remix v2 apps that need route actions, form submissions, fetcher mutations, pending-state handling, optimistic UI, multipart uploads, or multi-action routes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated file-upload handlers could preserve user-controlled filenames or accept unsafe uploads.

Mitigation: Use server-side random filenames, validate file contents after upload, enforce size and authorization limits, and clean up temporary files.

## Reference(s):

- [Remix V2 Forms on ClawHub](https://clawhub.ai/anderskev/skills/remix-v2-forms)
- [Form Reference](references/form.md)
- [useFetcher Reference](references/fetcher.md)
- [Optimistic UI Reference](references/optimistic-ui.md)
- [File Uploads Reference](references/uploads.md)
- [Intent Actions Reference](references/intent-actions.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Markdown]

**Output Format:** [Markdown guidance with TypeScript and TSX code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on Remix v2 mutation patterns; no shell execution or external service calls are required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
