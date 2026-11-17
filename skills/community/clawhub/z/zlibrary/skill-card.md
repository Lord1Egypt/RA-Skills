## Description:

Search and download books from Z-Library. Caches login session to ~/.zlibrary-session.json. Downloads book files (EPUB/PDF) to ~/Downloads/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imnoahcook](https://clawhub.ai/user/imnoahcook)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Z-Library by book metadata, inspect available formats, and download selected book files through an agent-assisted command workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles account credentials and cached Z-Library session tokens.

Mitigation: Use a unique password, restrict permissions on ~/.zlibrary-session.json, and delete the session cache when it is no longer needed.

Risk: The password may be briefly exposed in process arguments during login commands.

Mitigation: Run commands only in trusted local environments and avoid shared systems or process monitors when authenticating.

Risk: Downloads are written to ~/Downloads/ by default.

Mitigation: Specify another destination when needed and review downloaded files before opening or sharing them.

## Reference(s):

- [Z-Library ClawHub Skill Page](https://clawhub.ai/imnoahcook/skills/zlibrary)
- [Z-Library eAPI Login Endpoint](https://z-lib.sk/eapi/user/login)
- [Z-Library eAPI Book Search Endpoint](https://z-lib.sk/eapi/book/search)
- [Z-Library eAPI User Profile Endpoint](https://z-lib.sk/eapi/user/profile)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and numbered search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a reusable session cache to ~/.zlibrary-session.json and downloaded files to ~/Downloads/ unless another destination is specified.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
