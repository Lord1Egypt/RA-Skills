## Description:

Combine company results from Sales Navigator, AI Ark, Apollo, and Exa into a unified Cargo account layer, classify them against an ideal customer profile, and report CRM coverage, net-new accounts, and estimated market gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Revenue operations teams, GTM engineers, and sales leaders use this skill to adapt and run a multi-source TAM workflow in a Cargo project, compare provider results with their CRM, and identify net-new accounts and coverage gaps. The ICP, categories, source filters, and spend limits are set for each workspace before sourcing begins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious, citing that it installs a separate skill rather than providing the stated TAM workflow; the scan also reports security and privacy concerns and partial content inspection.

Mitigation: Before installation, review the installer and fetched skill at a pinned immutable version, verify the workflow and redirect handling, and confirm that CRM-derived data sharing and paid provider calls are approved.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cargo-ai/skills/tam-building-advanced)
- [Configure the ICP, source filters, and budget](artifact/references/configure.md)
- [Run sources and report results](artifact/references/run.md)
- [Source overview](artifact/references/sources.md)

## Skill Output:

**Output Type(s):** [Code, Configuration, Shell commands, SQL queries, Markdown guidance]

**Output Format:** [TypeScript project resources, configuration guidance, shell commands, SQL queries, and a written TAM report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The example must be adapted to the consumer Cargo workspace; sourcing and enrichment can incur usage charges.]

## Skill Version(s):

0.3.0 (source: frontmatter; server release evidence agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
