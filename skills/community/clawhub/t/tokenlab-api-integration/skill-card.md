## Description:

Guides developers through TokenLab API integration using current model contracts, runnable code, and reversible client configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hedging8563](https://clawhub.ai/user/hedging8563)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to select TokenLab endpoints from published model contracts, generate API integration code, and preview or apply supported agent-client configurations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying a client setup can change local configuration files.

Mitigation: Review the preview first; apply only when authorized and retain a path to restore the prior configuration.

Risk: Exposed API keys can permit unauthorized access.

Mitigation: Keep TOKENLAB_API_KEY in a local secret manager or process environment; never paste it into chat.

Risk: Live inference, media, or task calls may incur charges.

Mitigation: Confirm intent and expected cost before making live calls.

Risk: An unpinned installation source can change after review.

Mitigation: Install from a pinned, reviewed source rather than a mutable command.

## Reference(s):

- [TokenLab documentation](https://tokenlab.sh/docs)
- [TokenLab model catalog](https://api.tokenlab.sh/v1/models)
- [TokenLab OpenAPI specification](https://tokenlab.sh/docs/openapi.json)
- [Integration examples](references/integration_examples.md)
- [Codex setup guide](references/codex_setup.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with runnable code and commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint rationale, credential setup, error handling, and a verification command.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
