## Description:

Research new public-web backlink prospects for a website through comparable-brand link paths, relevant publishers, resources, listings, partnerships, and showcases, with existing mentions kept in a capped reclamation queue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvsao](https://clawhub.ai/user/lvsao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use this skill to research public-web backlink opportunities for a website, separate new prospects from existing-link reclamation, and prepare evidence-backed outreach queues without private store credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backlink prospect ledgers can be oversized or include low-quality reclamation entries that pass structural checks but still need SEO judgment.

Mitigation: Use the validator as a structural gate, then manually review evidence quality, relevance, reclamation share, and acquisition route before outreach.

Risk: Public-web research can encounter untrusted page content, unsafe redirects, private network destinations, or restricted pages.

Mitigation: Validate redirects and DNS results, reject local or reserved destinations, and respect robots directives, publisher terms, logins, paywalls, CAPTCHAs, and rate limits.

Risk: The skill could be misused to recommend paid links, link exchanges, mass submissions, spam directories, or unsupported claims about placement value.

Mitigation: Screen out link schemes and low-quality sources, keep exclusions visible, and avoid claiming a link is obtained, approved, dofollow, or valuable without public evidence.

## Reference(s):

- [Research protocol](references/research-protocol.md)
- [Project homepage](https://github.com/lvsao/shopify-skill-hub)
- [ClawHub skill page](https://clawhub.ai/lvsao/skills/seo-backlink-opportunity-finder)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with an opportunity ledger JSON and validator command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates new prospects from existing-link reclamation and reports the completed coverage tier, counts, omitted lanes, evidence URLs, and quality-risk notes.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
