## Description:

Guides agents in finding, validating, and downloading US state business registry data from public Socrata APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to locate state business registration datasets, assess their access terms and data quality, and fetch normalized records for analysis or entity matching.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Full registry downloads can take substantial time and disk space.

Mitigation: Start with --sample or limit the pull to one state and a smaller row count.

Risk: Downloaded registry records may include personal names and addresses, and reuse terms can vary by dataset.

Mitigation: Store downloaded records appropriately and verify the current terms for each source before commercial use.

## Reference(s):

- [Registry sources and dataset landing pages](artifact/references/sources.md)
- [Socrata SODA API query documentation](https://dev.socrata.com/docs/queries/)
- [Socrata app token documentation](https://dev.socrata.com/docs/app-tokens)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Files]

**Output Format:** [Markdown guidance, Python fetcher, and normalized JSON Lines data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The fetcher supports sample, state, and row-limit options; full downloads may be large.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
