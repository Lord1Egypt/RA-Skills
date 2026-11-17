## Description:

Enable SEO superpowers for OpenClaw. Get a massive boost in knowledge about technical SEO, content SEO, site structure, and measurement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realm1lf](https://clawhub.ai/user/realm1lf)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and site operators use this skill to guide SEO audits, crawling and indexing checks, metadata and structured-data reviews, site-structure improvements, and measurement hygiene. It supports German Google Search Central based guidance and optional user-directed HTTP diagnostics without promising search rankings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional HTTP checks may make requests to user-specified sites.

Mitigation: Allow curl only when the user wants site diagnostics and the gateway policy permits those requests.

Risk: API keys, tokens, or analytics credentials could be exposed if pasted into chat.

Mitigation: Keep secrets in environment variables or gateway configuration and refer to variable names only.

Risk: Copied JavaScript logging or telemetry examples may have privacy implications.

Mitigation: Review any logging snippet for data minimization, consent, and privacy requirements before deployment.

Risk: SEO guidance can become stale and rankings cannot be guaranteed.

Mitigation: Use primary search-engine documentation for current behavior and verify recommendations with measurable checks.

Risk: Maintainer packaging may rely on an unpinned validation command.

Mitigation: Pin skills-ref or use a local locked validator before packaging releases.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/realm1lf/skills/seo-expert-pro)
- [Google Search Central Documentation](https://developers.google.com/search/docs)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)
- [AgentSkills Specification](https://agentskills.io/specification)
- [Reference Index](references/OVERVIEW.md)
- [Authentication and Secrets Guidance](references/AUTH.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with checklists, explanations, and optional command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-directed curl-based HTTP checks when host policy allows.]

## Skill Version(s):

1.0.0 (source: server release metadata; bundle frontmatter reports 1.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
