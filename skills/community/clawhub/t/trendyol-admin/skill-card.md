## Description:

Comprehensive management of Trendyol marketplace via API v2.0, including product lifecycle, stock and price management, order processing, returns, and customer questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awelab](https://clawhub.ai/user/awelab)

### License/Terms of Use:


## Use Case:

Developers and marketplace operators use this skill as a knowledge base for constructing Trendyol Marketplace API v2.0 requests for store administration workflows.

### Deployment Geography for Use:

United Arab Emirates, Saudi Arabia, Qatar, Kuwait, Bahrain, Oman, Germany, Azerbaijan, Romania, Czech Republic, Hungary, Slovakia, Bulgaria, and Greece

## Known Risks and Mitigations:

Risk: Embedded Postman access_key URLs may expose credentials.

Mitigation: Remove or rotate embedded Postman access keys before distribution and avoid copying them into prompts, logs, or shared transcripts.

Risk: Credential-handling guidance may lead users to paste Trendyol API secrets into shell one-liners or shared transcripts.

Mitigation: Use environment variables or a secret manager, and avoid displaying raw API keys or secrets in generated commands.

Risk: API-assisted marketplace operations can modify product, order, invoice, webhook, and finance data.

Mitigation: Review generated requests before execution, test with stage credentials when available, and use accounts scoped to the intended store operations.

## Reference(s):

- [Trendyol Marketplace API Reference](references/api_reference.md)
- [Trendyol Developers Getting Started](https://developers.trendyol.com/v2.0/docs/getting-started)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API endpoints, JSON payload examples, headers, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No pre-built scripts; agents construct API requests from the reference material.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
