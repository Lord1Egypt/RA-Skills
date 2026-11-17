## Description:

Reads German municipal council records through the OParl API so agents can find endpoints, search and track council papers, monitor meetings, and generate reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yankhy-source](https://clawhub.ai/user/yankhy-source)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers, analysts, and civic-information users use this skill to query German municipal council records, follow the status of council papers, monitor new records on a subject, and create fileable summaries from public OParl data.

### Deployment Geography for Use:

Global; source data is German municipal council records.

## Known Risks and Mitigations:

Risk: Redirects can bypass the intended same-host network boundary for public OParl requests.

Mitigation: Use trusted OParl endpoints only and review redirect handling before installation or production use.

Risk: Untrusted logo PNG files are called out by the security guidance as unsafe until size limits are added.

Mitigation: Use only trusted local logo files for PDF reports, or omit the logo option.

Risk: The skill writes a local cache and can create user-named PDF or calendar files.

Mitigation: Run it in an expected working directory and review output paths before asking it to create files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yankhy-source/skills/ratsinfo-de)
- [Alpha Quadrat homepage](https://alpha-quadrat.de)
- [OParl](https://oparl.org/)
- [Legal footing and etiquette](references/recht-und-etikette.md)
- [RIS vendors and OParl URL patterns](references/vendors.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; the bundled CLI can return text or JSON and can write iCalendar or PDF files when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public OParl endpoints, a local cache, and optional user-named output files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
