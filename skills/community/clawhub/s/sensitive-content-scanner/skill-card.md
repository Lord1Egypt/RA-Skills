## Description:

Scans documents for sensitive content, prohibited words, and PII using built-in rules, custom keywords, or data dictionary files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinkai25](https://clawhub.ai/user/qinkai25)

### License/Terms of Use:

MIT-0

## Use Case:

Office staff, administrative users, document reviewers, compliance teams, and security reviewers use this skill to scan local documents for PII, sensitive words, prohibited terms, and weighted custom dictionary matches before sharing or publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may contain under-disclosed sensitive data from the scanned documents.

Mitigation: Protect generated report files, review them before sharing, and avoid JSON output for sensitive documents unless the raw PII behavior is fixed.

Risk: Generated reports may include undisclosed promotional contact content.

Mitigation: Review reports before external distribution and remove contact content that is not appropriate for the audience.

Risk: A generic scan request may be ambiguous about files, keywords, or output format.

Mitigation: Use a specific invocation that names the file or directory, requested keyword sources, and output format.

## Reference(s):

- [PII recognition patterns](references/pii_patterns.md)
- [Sensitive words hash library](references/sensitive_words_hashed.txt)
- [Custom sensitive words example](assets/custom_words_example.txt)
- [ClawHub skill page](https://clawhub.ai/qinkai25/skills/sensitive-content-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [HTML report by default, with optional Markdown or JSON report output and command-line guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports summarize file-level findings, risk levels, PII matches, sensitive word matches, and weighted dictionary matches.]

## Skill Version(s):

3.2.0 (source: server release evidence and script header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
