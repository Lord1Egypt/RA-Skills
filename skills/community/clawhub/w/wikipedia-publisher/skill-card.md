## Description:

Draft, review, de-risk, and publish Wikipedia or Wikidata content with a policy-safe workflow for encyclopedia articles, sandbox drafts, citations, notability/source assessments, conflict-of-interest reviews, and MediaWiki wikitext.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colto111](https://clawhub.ai/user/colto111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and agents use this skill to prepare Wikipedia and Wikidata drafts, assess source quality and notability, reduce promotional or conflict-of-interest risk, and choose sandbox or draft publishing paths before live edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sandbox publishing helper can send wiki credentials to a user-supplied MediaWiki API endpoint.

Mitigation: Use dry-run first, avoid command-line passwords, and do not set WIKI_USERNAME or WIKI_PASSWORD when using a custom --api endpoint.

Risk: The citation URL enricher fetches arbitrary URLs without network safety bounds.

Mitigation: Run URL enrichment only on trusted public URLs or inside a network-restricted environment.

## Reference(s):

- [Citation Guidelines](references/citation-guidelines.md)
- [Wikipedia Publishing Red Flags](references/red-flags.md)
- [Workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with MediaWiki wikitext, citation templates, JSON helper output, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sandbox or draft recommendations, source-quality scores, notability signals, risk flags, and dry-run publishing instructions.]

## Skill Version(s):

0.3.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
