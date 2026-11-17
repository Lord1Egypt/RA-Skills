## Description:

Guides agents in collecting and analyzing public LinkedIn Ad Library data through SocQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and marketing teams use this skill to find and compare public LinkedIn ads, collect ad details, and summarize results or retrieve raw exports through SocQ.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted ad-library queries and task metadata are sent to SocQ.

Mitigation: Confirm the user trusts SocQ with the submitted data before use and keep the API key out of prompts, URLs, and stored commands.

Risk: Large or repeated collections can incur credits.

Mitigation: Check live pricing and available limits, estimate the cost, and obtain confirmation before large-volume or multi-endpoint runs.

Risk: Ad hoc CLI execution may introduce supply-chain exposure.

Mitigation: Prefer an existing installation or a pinned @socq/cli version over ad hoc npx execution in stricter environments.

## Reference(s):

- [SocQ LinkedIn Ad Library API documentation](https://docs.socq.ai/api-manual/linkedin-ad-library)
- [SocQ integrations overview](https://docs.socq.ai/integrations/overview)
- [SocQ agent skill guide](https://docs.socq.ai/integrations/skill)
- [SocQ developer tools](https://github.com/SocQAPI/socq-devtools)
- [Endpoint selection and pricing](artifact/references/platform.md)
- [Billing and cost control](artifact/references/billing.md)
- [Asynchronous tasks](artifact/references/async-tasks.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text, Files]

**Output Format:** [Markdown summaries with optional raw JSONL export location]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint, filters, credit usage, task status, result count, pagination, and coverage caveats when available.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
