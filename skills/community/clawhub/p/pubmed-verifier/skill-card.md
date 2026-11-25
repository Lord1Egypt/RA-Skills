## Description:

Verifies PMIDs, DOIs, arXiv IDs, and reference lists against academic registries, checking whether each identifier matches the cited paper and producing citation reports and formatted references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[docsor1212](https://clawhub.ai/user/docsor1212)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, medical writers, and evidence-based medicine teams use it to audit reference lists and check whether cited identifiers point to the papers they claim.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reported citation-verification flaws could miss mismatches or misclassify lookup failures, and the security review is partial.

Mitigation: Use the results as an aid rather than the sole accuracy check; confirm important citations against the source paper or registry.

Risk: The skill sends citation data in requests to external registries, and disclosure may be inadequate.

Mitigation: Avoid submitting confidential citation information unless you understand and accept the external data flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/docsor1212/skills/pubmed-verifier)
- [Project homepage](https://github.com/docsor1212/pubmed-verifier)
- [Usage guide](references/usage_guide.md)
- [API examples](references/api_examples.md)

## Skill Output:

**Output Type(s):** [Text, JSON, HTML]

**Output Format:** [Citation verification reports in text, JSON, or HTML, plus formatted reference lists.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verification results use correct, mismatch, partial, invalid, or unknown states; registry failures are reported as unverified.]

## Skill Version(s):

7.2.1 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
