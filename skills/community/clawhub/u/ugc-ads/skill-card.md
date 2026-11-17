## Description:

Generates guidance, prompts, cost checks, and shell commands for creating deliberately unpolished, phone-shot UGC-style product video clips through Ofox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ofoxai](https://clawhub.ai/user/ofoxai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and marketing teams use this skill to prepare realistic customer-style product video generation requests, including product-photo handling, prompt structure, pricing dry-runs, and approval-gated paid generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an Ofox API key and can send prompts, optional product images, and paid generation requests to Ofox.

Mitigation: Keep the API key in the environment, avoid placing it in prompts, and review the request data before using billable commands.

Risk: Paid generation commands can create spend if run without a user-reviewed quote.

Mitigation: Require a dry-run cost table and explicit approval before any command that includes --approved.

Risk: The artifact documents an npx recovery command path that can affect local skill installation if copied and run without review.

Mitigation: Review any npx recovery command before running it and relay installation commands for the user to execute intentionally.

Risk: Generated clips may drift toward polished ad aesthetics or include a flash cut when a product photo background conflicts with the target scene.

Mitigation: Check outputs for polish creep, match product-photo setting to the scene when possible, and consider trimming the first 0.15 seconds if a flash frame appears.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ofoxai/skills/ugc-ads)
- [Publisher profile](https://clawhub.ai/user/ofoxai)
- [Ofox app and API keys](https://app.ofox.ai)
- [Skill homepage](https://github.com/ofoxai/skills/tree/main/skills/ugc-ads)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and structured decision guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run cost tables, approval-gated generation commands, prompt drafts, and local file handling guidance.]

## Skill Version(s):

2.0.0 (source: server release metadata, skill frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
