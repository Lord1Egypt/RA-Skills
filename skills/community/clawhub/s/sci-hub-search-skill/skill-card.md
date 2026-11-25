## Description:

AI-powered tool for searching and downloading academic papers through Sci-Hub

This skill is for research and development only.

## Publisher:

[jackkuo666](https://clawhub.ai/user/jackkuo666)

### License/Terms of Use:

MIT

## Use Case:

Researchers and developers use this skill to search for academic papers by DOI, title, or keyword, retrieve metadata, and optionally download PDFs through Sci-Hub. Use requires review for copyright, organizational policy, and jurisdiction-specific legality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, paper titles, and DOIs may be sent to CrossRef and Sci-Hub.

Mitigation: Run searches only for non-sensitive queries and only when Sci-Hub use is legal and acceptable for the user, jurisdiction, and organization.

Risk: Download commands can write retrieved PDFs or command output to local paths.

Mitigation: Use a dedicated download directory, avoid sensitive or arbitrary output paths, and review downloaded files before sharing or opening them.

Risk: Installation and dependency setup can grant local and network authority, especially when using remote installer commands.

Mitigation: Prefer a local virtual environment, pin dependencies and release revisions, and review the skill before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackkuo666/skills/sci-hub-search-skill)
- [Crossref Works API](https://api.crossref.org/works)
- [Sci-Hub](https://sci-hub.se)
- [scihub PyPI package](https://pypi.org/project/scihub/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, files, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, console text, JSON records, and downloaded PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DOI, title, author, year, PDF URL, status fields, and local output paths.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
