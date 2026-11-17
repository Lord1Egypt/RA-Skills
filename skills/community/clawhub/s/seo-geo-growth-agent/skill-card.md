## Description:

Read-only SEO and GEO opportunity analysis with evidence-backed backlog output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[replynodes-ai](https://clawhub.ai/user/replynodes-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Growth marketers, SEO teams, and agents use this skill to run read-only SEO/GEO audits, competitor gap analysis, opportunity prioritization, and content brief preparation from supplied or allowlisted sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user may ask the skill to publish, schedule, edit, send, or write to a production system.

Mitigation: Refuse the write request and return a reviewable backlog item or content brief for an explicitly authorized downstream workflow.

Risk: Insufficient source material or read-only capability gaps could lead to unsupported SEO, traffic, ranking, or citation claims.

Mitigation: Use only supplied or allowlisted read-only sources, record unavailable signals as limitations, and return SKIP when evidence is insufficient.

Risk: SEO or analytics workflows can accidentally expose credentials, cookies, tokens, customer data, or private operational data.

Mitigation: Do not request, store, reveal, or use secrets, and keep analysis constrained to explicitly allowed read-only evidence.

## Reference(s):

- [Capability Detection](references/capability-detection.md)
- [ClawHub Skill Page](https://clawhub.ai/replynodes-ai/skills/seo-geo-growth-agent)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Structured text and Markdown backlog artifacts, with YAML-style proposed backlog item templates when useful.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only recommendations only; no automatic publishing, CMS edits, analytics changes, credential handling, telemetry, or backlog writes.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
