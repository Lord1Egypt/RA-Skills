## Description:

Cascade contact or company enrichment across providers in priority order, then verify returned email addresses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Revenue operations and GTM engineering teams use this skill to enrich contact or company records through provider fallbacks, verify returned email addresses, and control credit spend with small sample runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact and company records may be sent to external enrichment providers, and batch costs grow with the number of records.

Mitigation: Confirm you are authorized to share the records, sample 10–20 records, and review hit rate and credit cost before running a full batch.

Risk: The install command uses the unpinned @latest CLI package, and the workflow includes email-verification and repository-starring prompts.

Mitigation: Review and trust the package source before installation; proceed with verification or starring only when those actions match your intent.

## Reference(s):

- [Cargo skill repository homepage](https://github.com/getcargohq/gtm-skills)
- [Cargo waterfall provider playbook](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/provider-playbooks/waterfall.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Analysis]

**Output Format:** [Markdown with inline shell commands and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can start asynchronous enrichment batches and incur per-record credit costs.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
