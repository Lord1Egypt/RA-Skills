## Description:

Web of Science literature search and download assistant that helps users search WOS, extract publication metadata, and download or organize PDFs for environmental psychology and restorative environment research when they have valid institutional access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziyi-z-z](https://clawhub.ai/user/ziyi-z-z)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and research-support developers use this skill to prepare Web of Science searches, parse exported literature records, check open-access availability, and organize paper metadata and download lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DOI lookups are sent to Unpaywall and may disclose research interests or paper identifiers to a third-party API.

Mitigation: Use the skill only when that disclosure is acceptable, and avoid submitting sensitive or embargoed research queries through third-party lookup services.

Risk: The downloader writes PDFs from URLs returned by a third-party API without URL allowlisting, download size limits, or PDF validation.

Mitigation: Run it in a dedicated virtual environment with a limited output folder, inspect downloaded PDFs before opening them, and add URL validation and size limits before broader deployment.

Risk: Generated CSV and JSON metadata files are built from exported literature records and should be treated as untrusted data.

Mitigation: Review generated files before importing them into spreadsheets, scripts, or downstream research systems.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ziyi-z-z/skills/wos-paper-downloader)
- [Web of Science Advanced Search Guide](references/wos_search_guide.md)
- [DOI Resolver and Open Access Checks](references/doi_resolver.md)
- [API Reference](references/api_reference.md)
- [Web of Science](https://www.webofscience.com)
- [Unpaywall API](https://api.unpaywall.org/v2/{doi}?email={your_email})
- [Crossref Works API](https://api.crossref.org/works/{doi})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated local CSV, JSON, text, and PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Web of Science search instructions, metadata files, subscription download lists, and open-access PDF downloads when permitted.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
