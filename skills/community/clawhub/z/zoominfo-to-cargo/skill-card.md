## Description:

Rebuild a ZoomInfo, Lusha, or Cognism contact list on Cargo and compare verified coverage and credits before renewal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Revenue operations teams and sales leaders use this skill to evaluate whether a ZoomInfo, Lusha, or Cognism renewal is worthwhile. It guides a small contact sample through enrichment and email verification, then compares verified coverage and estimated credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact records may be processed by Cargo and its enrichment providers, including the initial sample.

Mitigation: Use only records approved for processing, and check provider data practices before running the comparison.

Risk: Expanding a batch beyond the sample can increase credit costs with the number of records.

Mitigation: Start with 10–20 records, report the observed cost, and get approval using the record count and credit estimate before a full run.

Risk: The external CLI and optional skill pack are outside the reviewed artifact.

Mitigation: Review their contents before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cargo-ai/skills/zoominfo-to-cargo)
- [Cargo project homepage](https://github.com/getcargohq/gtm-skills)
- [Waterfall provider playbook](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/provider-playbooks/waterfall.md)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Guidance, Markdown]

**Output Format:** [Markdown comparison with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports sampled verified coverage for both providers and the credits used or estimated.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
