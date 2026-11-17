## Description:

Candidate discovery for link building and outreach that harvests candidate URLs from DuckDuckGo HTML and Marginalia through a local Tor circuit, deduplicates and triages them, and exports a scored candidate list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toniilic](https://clawhub.ai/user/toniilic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and outreach operators use this skill to find candidate directories, submission platforms, blogs, and link-building opportunities. It is scoped to discovery and triage, not posting, submitting forms, creating accounts, or changing third-party sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and harvested URLs may be exposed to third-party Tor exit infrastructure.

Mitigation: Use only after explicit approval for Tor routing, and avoid sensitive, personal, client-identifying, or proprietary queries.

Risk: Automated search access may implicate search-engine terms or trigger blocks if run at high volume.

Mitigation: Keep runs low-volume and rate-limited, rotate as documented, and stop when engines degrade or block requests.

Risk: Generated reports can contain sensitive prospecting data.

Mitigation: Write reports to a private directory and review them before sharing.

Risk: Discovery results can be mistaken for approval to submit forms or change third-party sites.

Mitigation: Treat output as candidate research only; use a separate workflow with explicit per-site consent for any downstream submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/toniilic/skills/search-harvester)
- [Project homepage](https://github.com/toniilic/scraper-skill)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with ranked candidate URLs, liveness or barrier status, and query provenance for each candidate.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes only to an explicit output path and refuses to overwrite existing reports unless forced.]

## Skill Version(s):

1.0.2 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
