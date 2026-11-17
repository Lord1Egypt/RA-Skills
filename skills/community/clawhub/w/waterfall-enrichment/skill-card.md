## Description:

Routes contact or company lookups through prioritized vendors, trying later providers when earlier ones find no match.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

RevOps and GTM engineering teams use the CLI to enrich contact or company records with prioritized provider fallback. They can verify returned email addresses and estimate cost on a sample before processing a full list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact records may include personal information shared with Cargo and its providers.

Mitigation: Use only records you are authorized to share, including the initial sample.

Risk: A full batch can incur substantial credit costs as charges scale with records processed.

Mitigation: Start with a 10–20 record sample, review observed cost and hit rate, then approve the full batch using its record count and credit estimate.

Risk: The CLI package and optional Cargo pack are external dependencies whose contents are not included with this skill.

Mitigation: Review their versions and contents separately before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/cargo-ai/skills/waterfall-enrichment)
- [Declared skill homepage](https://github.com/getcargohq/gtm-skills)
- [Cargo waterfall provider playbook](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/provider-playbooks/waterfall.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown instructions with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use fictional records; batch costs vary with record count.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
