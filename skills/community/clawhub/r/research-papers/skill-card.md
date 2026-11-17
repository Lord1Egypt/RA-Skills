## Description:

Search academic papers and generate literature-review support using OpenAlex, with defaults tailored to dynamic brain networks, fMRI neuroimaging, graph neural networks, and neurodegenerative disease classification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjuncher](https://clawhub.ai/user/zjuncher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to search papers, look up DOIs, inspect citation chains, discover open-access links, and draft Markdown literature reviews. The default research context is neuroimaging and dynamic brain network modeling for neurodegenerative disease classification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional QQBot handoff can execute a caller-selected local Python staging script.

Mitigation: Use --qqmedia and --stage-media-script only with a trusted, package-owned staging script path; review the handoff before installing or running this option.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zjuncher/skills/research-papers)
- [OpenAlex API](https://api.openalex.org)
- [Unpaywall API](https://api.unpaywall.org/v2)
- [DOI resolver](https://doi.org/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands, guidance]

**Output Format:** [Plain text, Markdown, JSON, saved Markdown files, and optional qqmedia tags.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cache API responses locally, save literature-review files, and optionally hand off generated review files through QQBot.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
