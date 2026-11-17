## Description:

Analyzes website structure and generates RSSHub-compatible TypeScript route code, selector configuration, optional full-text RSS support, and Radar rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benzking](https://clawhub.ai/user/benzking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to inspect a target website and produce RSSHub route implementation files, selector notes, and routing metadata for a new RSS feed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated RSSHub routes may perform server-side requests to article links derived from untrusted websites.

Mitigation: Review generated routes before deployment and add URL validation, explicit host allowlists, redirect checks, private-network blocking, timeouts, and response-size limits.

Risk: Full-text fetching can expand the number of outbound requests made by deployed route code.

Mitigation: Keep full-text fetching opt-in and use bounded concurrency before enabling generated code on an RSSHub server.

## Reference(s):

- [RSSHub Route Development Reference](artifact/references/dev-guide.md)
- [ClawHub Skill Release Page](https://clawhub.ai/benzking/skills/rsshub-route-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown analysis report with TypeScript route code and RSSHub configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated route files under rsshub-routes, namespace files, selector mappings, and optional full-text fetching logic.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
