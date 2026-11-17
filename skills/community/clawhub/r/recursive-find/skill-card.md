## Description:

Search a site from a starting page to find pages mentioning a query, returning matching URLs with short context snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grtwrn](https://clawhub.ai/user/grtwrn)

### License/Terms of Use:

MIT

## Use Case:

Developers and researchers use this skill to locate mentions of a topic across linked pages of a website or documentation section without reading every page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following redirects may contact sites outside the intended boundary, including internal network services.

Mitigation: Use only sites you intend the agent host to contact; validate redirects and block private, loopback, link-local, and other internal network targets.

## Reference(s):

- [Recursive Find on ClawHub](https://clawhub.ai/grtwrn/skills/recursive-find)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Plain-text results or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matching page URLs and short highlighted snippets; reports when page or time limits truncate the search.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
