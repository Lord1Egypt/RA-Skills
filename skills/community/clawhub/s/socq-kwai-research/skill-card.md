## Description:

Helps agents collect and analyze public Kwai posts, profiles, and user posts through SocQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to collect public Kwai posts and profiles, choose SocQ endpoints, manage credit-metered tasks, and summarize results or locate raw exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SocQ requests use an API key with hosted tools.

Mitigation: Keep SOCQ_API_KEY in the environment; do not place it in prompts, URLs, or saved commands.

Risk: Large or repeated jobs can consume credits.

Mitigation: Estimate costs and obtain confirmation before paid large-volume or multi-endpoint runs; inspect failures before retrying.

Risk: The CLI fallback may fetch an unpinned latest package.

Mitigation: Pin or preinstall a vetted @socq/cli version before using the fallback.

## Reference(s):

- [SocQ Kwai API documentation](https://docs.socq.ai/api-manual/kwai)
- [SocQ integrations overview](https://docs.socq.ai/integrations/overview)
- [SocQ developer tools homepage](https://github.com/SocQAPI/socq-devtools)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with results, task status, credit use, and optional command snippets or export locations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports endpoint, filters, result counts, pagination, collection time, and coverage limits.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
