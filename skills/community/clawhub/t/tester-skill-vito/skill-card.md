## Description:

Run outcome-focused Firecrawl workflows that produce deliverables such as research reports, SEO audits, QA reports, lead lists, knowledge bases, website design systems, and other structured web-data artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vitobigbrain](https://clawhub.ai/user/vitobigbrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route Firecrawl-backed web research and site analysis requests into finished business, marketing, product, or creative deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Firecrawl-backed workflows can send URLs, page content, and user-provided research inputs to an external collection service.

Mitigation: Avoid sensitive internal URLs, private documents, regulated data, and credential-bearing pages unless the user is authorized and accepts Firecrawl processing.

Risk: The workflow requires a Firecrawl API key when executed through hosted Firecrawl surfaces.

Mitigation: Use normal secret-management practices and avoid placing API keys in committed files, public transcripts, or generated deliverables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vitobigbrain/skills/tester-skill-vito)
- [Firecrawl](https://www.firecrawl.dev)
- [Firecrawl workflows source](https://github.com/firecrawl/firecrawl-workflows)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with structured deliverables and rerun inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source evidence, recommendations, and automation inputs for reruns.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
