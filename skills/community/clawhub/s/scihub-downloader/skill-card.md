## Description:

Download academic papers from multiple sources including Unpaywall, PubMed Central, Semantic Scholar, arXiv, and Sci-Hub with direct PDF link extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doradx](https://clawhub.ai/user/doradx)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and research automation agents use this skill to locate and download academic paper PDFs from open-access services, arXiv, and configured Sci-Hub mirrors by DOI, PMID, arXiv ID, URL, or title.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically falls back to Sci-Hub and documents mirror or VPN access, which may create copyright or policy risk in some environments.

Mitigation: Review before installing in workplace, school, or compliance-sensitive environments and use --oa-only unless the paper source is lawful for the user.

Risk: Paper titles, DOIs, and related identifiers may be sent to multiple external services and Sci-Hub mirrors.

Mitigation: Avoid sensitive research queries unless disclosure to those external services is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/doradx/skills/scihub-downloader)
- [DOI Format Reference](references/doi-formats.md)
- [Sci-Hub Mirrors Reference](references/mirrors.md)
- [Usage Examples](references/usage-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command examples and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write PDF files to a user-selected output directory and can emit metadata as JSON when invoked with --json.]

## Skill Version(s):

3.1.0 (source: server release evidence and artifact package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
