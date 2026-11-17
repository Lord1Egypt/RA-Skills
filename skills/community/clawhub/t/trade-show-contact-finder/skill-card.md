## Description:

Trade Show Contact Finder helps agents search Lensmor contact records by company and optional role or person name, then summarize returned contact fields and lock states.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilun88313](https://clawhub.ai/user/weilun88313)

### License/Terms of Use:

MIT-0

## Use Case:

External users and sales or event teams use this skill to find relevant contacts at exhibitor companies before a trade show. The skill is intended to return API-backed contact records, preserve lock-state semantics, and avoid unsupported claims about decision authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports an unpinned third-party install command that acknowledges a ClawHub risk warning.

Mitigation: Review package provenance before installing and prefer a pinned audited release.

Risk: The skill requires LENSMOR_API_KEY and may be invoked by broad contact-finding phrases.

Mitigation: Only provide the API key when the agent is intended to query Lensmor, keep the key secret, and confirm broad contact-finding requests before making API calls.

Risk: Contact results can include professional contact fields and already-unlocked emails.

Mitigation: Report returned lock states accurately, avoid unlock workflows, and expose unlocked contact details only when the user explicitly requests them in the current workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/weilun88313/skills/trade-show-contact-finder)
- [Lensmor API Docs](https://api.lensmor.com/)
- [Lensmor Contact Search Endpoint](https://platform.lensmor.com/external/contacts/search)
- [Lensmor](https://www.lensmor.com/?utm_source=github&utm_medium=skill&utm_campaign=trade-show-skills)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Guidance]

**Output Format:** [Markdown contact summaries with tables, priority notes, and contact lock-state status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LENSMOR_API_KEY; does not unlock email or phone data; preserves returned contact fields and seniority values.]

## Skill Version(s):

1.2.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
