## Description:

Migrate OpenAI-compatible apps, SDKs, examples, and environment variables to TokenLab while preserving request semantics and adding live model discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hedging8563](https://clawhub.ai/user/hedging8563)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to migrate OpenAI-compatible integrations, SDK wrappers, examples, and environment variables to TokenLab with minimal code or configuration changes. It helps preserve existing request semantics, add live model discovery, provide smoke tests, and document rollback steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unreviewed migration changes could introduce incorrect provider configuration or alter application behavior.

Mitigation: Review the generated diff, migrate one API family at a time when integrations have separate endpoints, and run the provided smoke test before deployment.

Risk: API keys could be exposed if copied into source files or prompts during migration.

Mitigation: Keep credentials in environment variables such as TOKENLAB_API_KEY and avoid embedding secrets in code or prompts.

Risk: Installing from a moving source can make the reviewed skill version hard to reproduce.

Mitigation: Pin the skill source to a reviewed commit and avoid non-interactive installation flags when review is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hedging8563/skills/tokenlab-openai-compatible-migration)
- [TokenLab OpenAI-compatible API base URL](https://api.tokenlab.sh/v1)
- [TokenLab model discovery endpoint](https://api.tokenlab.sh/v1/models)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with focused diffs, configuration blocks, runnable snippets, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include one migration-surface explanation, one smoke test command, one model discovery command, and one rollback line.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
