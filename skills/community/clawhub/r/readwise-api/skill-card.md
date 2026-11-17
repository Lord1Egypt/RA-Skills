## Description:

Manage Readwise highlights, books, daily review, and Reader documents (save-for-later / read-it-later).

This skill is ready for commercial/non-commercial use.

## Publisher:

[gchapim](https://clawhub.ai/user/gchapim)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to save, search, list, update, and delete Readwise Reader documents, and to review or manage Readwise highlights, books, notes, tags, and daily review items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe command argument handling may allow untrusted text or prompts to influence Readwise CLI operations.

Mitigation: Only run commands after reviewing the generated arguments, and do not let untrusted page content choose command options or identifiers.

Risk: Delete commands for Reader documents and Readwise highlights execute immediately.

Mitigation: Require explicit user confirmation before delete actions, and use a revocable Readwise token with the least practical account exposure.

Risk: Unvalidated numeric limits can lead to unexpected API usage or rate-limit pressure.

Mitigation: Use conservative --limit values and add strict numeric validation before broad deployment.

## Reference(s):

- [Readwise & Reader API Reference](references/api.md)
- [Readwise API Token](https://readwise.io/access_token)
- [ClawHub Skill Page](https://clawhub.ai/gchapim/skills/readwise-api)
- [ClawHub Publisher Profile](https://clawhub.ai/user/gchapim)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with bash command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and a READWISE_TOKEN environment variable; commands call Readwise and Reader APIs and can modify or delete account data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
