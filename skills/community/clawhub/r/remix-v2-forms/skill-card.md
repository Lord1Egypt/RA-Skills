## Description: <br>
Remix v2 form submissions and mutations. Use when implementing forms, optimistic UI, file uploads, or multi-action routes. Triggers on <Form>, useFetcher, useSubmit, useNavigation for pending state, unstable_parseMultipartFormData, fetcher.formData, intent-based actions, encType multipart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to implement Remix v2 mutations with route actions, progressive-enhanced forms, pending state, optimistic UI, file uploads, and multi-action intent routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Adapted upload examples can expose applications to oversized files, unsafe file names, or untrusted content. <br>
Mitigation: Apply explicit upload size and type limits, sanitize filenames, validate content, and use a storage strategy appropriate for expected file sizes. <br>
Risk: Mutation examples for delete or state-changing actions can be unsafe if copied without application checks. <br>
Mitigation: Add authorization, schema validation, and explicit confirmation for destructive actions before integrating examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/remix-v2-forms) <br>
- [Form component reference](references/form.md) <br>
- [useFetcher reference](references/fetcher.md) <br>
- [Intent-based actions reference](references/intent-actions.md) <br>
- [Optimistic UI reference](references/optimistic-ui.md) <br>
- [File uploads reference](references/uploads.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code] <br>
**Output Format:** [Markdown guidance with TypeScript and TSX code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no hidden execution behavior according to security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
