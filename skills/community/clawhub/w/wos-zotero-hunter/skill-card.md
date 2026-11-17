## Description:

Search Web of Science through institutional access, filter scholarly literature by journal, impact factor, citation count, or date, and import selected results into a Zotero collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanfanliu964-web](https://clawhub.ai/user/fanfanliu964-web)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and literature-reviewing agents use this skill to search Web of Science with quality filters, review extracted paper metadata, and import selected records into a new Zotero collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles a read/write Zotero API key.

Mitigation: Use a narrowly scoped Zotero API key, avoid pasting the key directly into command lines, and rotate the key if it may have been exposed.

Risk: Browser automation may use the user's authenticated Web of Science session.

Mitigation: Run the browser steps only in the intended profile and confirm institutional access before allowing the agent to continue.

Risk: Crossref lookups disclose paper titles or DOIs to an external metadata service.

Mitigation: Review the candidate paper list first and proceed only when sharing titles or DOIs with Crossref is acceptable.

Risk: The import writes records into the user's Zotero library.

Mitigation: Run with --dry-run first and review extracted papers before authorizing the final import.

## Reference(s):

- [WoS Zotero Literature Hunter on ClawHub](https://clawhub.ai/fanfanliu964-web/skills/wos-zotero-hunter)
- [Zotero API Keys](https://www.zotero.org/settings/keys)
- [Crossref Works API title lookup](https://api.crossref.org/works?query.title={query}&rows=1)
- [DOI resolver](https://doi.org/{doi})

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON paper metadata and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce a dry-run preview and an import summary before writing selected records to Zotero.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
