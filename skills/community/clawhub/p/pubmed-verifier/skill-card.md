## Description:

Verifies PMID, DOI, arXiv, and reference-list citations against academic registries, comparing claimed metadata with source records and reporting uncertain checks explicitly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[docsor1212](https://clawhub.ai/user/docsor1212)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, medical writers, and evidence-based teams use the skill to check whether cited PMIDs, DOIs, arXiv identifiers, and reference lists exist and match the claimed publications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Citation identifiers, titles, search terms, and an optional contact email may be sent to external academic registries during checks.

Mitigation: Avoid submitting sensitive unpublished queries, and omit the optional contact email unless needed.

Risk: Unusual reference formatting or incomplete registry responses can leave citation verdicts uncertain or incomplete.

Mitigation: Treat unknown results as unresolved, review partial or mismatch results against source records, and provide structured claims with expected titles when a more decisive check is needed.

Risk: The skill makes outbound requests to academic registries, so its network access should fit the host's policy.

Mitigation: Confirm that the host permits requests to the registries needed for the verification task.

## Reference(s):

- [PubMed Verifier on ClawHub](https://clawhub.ai/docsor1212/skills/pubmed-verifier)
- [Project homepage (package metadata)](https://github.com/docsor1212/pubmed-verifier)
- [Usage guide](references/usage_guide.md)
- [API examples](references/api_examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, JSON, CSV, BibTeX, RIS, CSL JSON]

**Output Format:** [Terminal summaries and citation reports or bibliography files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports use correct, mismatch, partial, invalid, and unknown verdicts; network failures are reported as unverified.]

## Skill Version(s):

7.0.0 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
