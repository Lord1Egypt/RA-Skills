## Description:

Guides agents through collecting and analyzing public Instagram data using SocQ, including endpoint selection, credit estimates, task polling, and pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to collect and compare public Instagram accounts, posts, reels, and related data through SocQ, with cost checks and clear reporting of incomplete results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public Instagram queries and API-key billing context are sent to SocQ.

Mitigation: Use only with a trusted SocQ account, keep the key out of prompts and logs, and configure spending limits.

Risk: Large or repeated credit-metered jobs can incur unexpected charges.

Mitigation: Review cost estimates and obtain confirmation before large or multi-endpoint runs; avoid blindly retrying paid requests.

Risk: Unpinned CLI installation may run code that changes independently of this skill.

Mitigation: Prefer a pinned or preinstalled SocQ CLI in controlled environments.

## Reference(s):

- [SocQ Instagram API documentation](https://docs.socq.ai/api-manual/instagram)
- [SocQ integration overview](https://docs.socq.ai/integrations/overview)
- [SocQ agent skill guide](https://docs.socq.ai/integrations/skill)
- [SocQ CLI repository (metadata homepage)](https://github.com/SocQAPI/socq-devtools)
- [Instagram endpoint reference in skill](artifact/references/platform.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown research summary with normalized findings or a raw export location]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint, cost, task status, result count, collection time, and coverage caveats when available.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
