## Description:

Uses a connected Scholar Sidekick MCP server to resolve scholarly identifiers, format citations, export bibliography data, check retraction and open-access status, and verify whether citation claims are real.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mlava](https://clawhub.ai/user/mlava)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, authors, clinicians, and agents handling scholarly references use this skill to turn known identifiers into metadata, citations, bibliography exports, retraction checks, open-access checks, and citation-verification answers. It is intended for identifier-based scholarly workflows rather than topic search or citation-network exploration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external Scholar Sidekick MCP/API service and a RAPIDAPI_KEY, so unintended connection or overly broad credentials can create unnecessary exposure.

Mitigation: Connect the service only when it is needed, keep the RAPIDAPI_KEY limited to this server, and run the MCP server in a least-privilege environment.

Risk: Using an unpinned npx server command can introduce supply-chain drift between review and installation.

Mitigation: Prefer a reviewed pinned package version such as `scholar-sidekick-mcp@<reviewed-version>`.

## Reference(s):

- [Scholar Sidekick homepage](https://scholar-sidekick.com)
- [Scholar Sidekick RapidAPI service](https://rapidapi.com/scholar-sidekick-scholar-sidekick-api/api/scholar-sidekick)
- [Citation Style Language styles](https://github.com/citation-style-language/styles)
- [ClawHub skill page](https://clawhub.ai/mlava/skills/scholar-sidekick-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown responses with citation text, structured metadata summaries, bibliography export content, and MCP configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected scholar-sidekick-mcp server with RAPIDAPI_KEY for tool-backed results; export formats include BibTeX, RIS, CSL JSON, EndNote, RefWorks, Medline, Zotero RDF, CSV, and plain text.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
