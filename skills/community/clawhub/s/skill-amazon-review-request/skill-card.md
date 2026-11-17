## Description:

Sends Amazon review requests for eligible shipped orders using SP-API with retry, deduplication, eligibility checks, and optional dry-run mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT

## Use Case:

Amazon marketplace operators use this skill to request reviews for eligible shipped orders, test runs with a dry-run mode, and keep local tracking logs for sent, skipped, and failed requests.

### Deployment Geography for Use:

Global, with default configuration targeting Amazon's EU SP-API endpoint for the UAE marketplace.

## Known Risks and Mitigations:

Risk: Order-processing metadata can be sent to a Supabase project when Supabase credentials are present, and that behavior is not clearly disclosed in the user-facing instructions.

Mitigation: Install only after confirming the Supabase endpoint, making the behavior explicit and opt-in, and using a trusted project with a least-privilege key.

Risk: Live runs use Amazon SP-API Messaging permissions to send review requests for eligible orders.

Mitigation: Run in dry-run mode first, verify the eligibility window and deduplication results, and schedule live execution only with scoped SP-API credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-amazon-review-request)
- [Publisher profile](https://clawhub.ai/user/zero2ai-hub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, configuration examples, and run-summary text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local JSON and text logs during execution; live mode sends SP-API Messaging requests.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
