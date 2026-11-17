## Description:

Lists exhibitor records for a specific trade show or searches Lensmor's wider exhibitor dataset from a company URL or target-audience phrase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilun88313](https://clawhub.ai/user/weilun88313)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, marketing, and event teams use this skill to find Lensmor exhibitor records for named trade shows or discover exhibitor companies across the Lensmor dataset. It helps preserve boundaries between event-scoped records and cross-event discovery while reporting preview, access, and ranking evidence accurately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company URLs, target-audience phrases, event names, and filters are sent to Lensmor when the skill calls Lensmor API endpoints.

Mitigation: Use the skill only for intended Lensmor exhibitor research and avoid submitting information that should not be shared with Lensmor.

Risk: Unlocking additional event-scoped exhibitor records can consume credits.

Mitigation: Confirm the unlock action type and exact credit cost with the user before any unlock action.

Risk: Cross-event discovery results can be mistaken for evidence that a company exhibits at a named event.

Mitigation: Keep event-specific and cross-event modes separate and only claim event association when returned fields such as matched_event_ids support it.

Risk: API credentials could be exposed if echoed in output or logs.

Mitigation: Check only that LENSMOR_API_KEY is configured and never print the key value or raw authorization headers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/weilun88313/skills/trade-show-exhibitor-search)
- [Lensmor API Docs](https://api.lensmor.com/)
- [Lensmor Platform](https://platform.lensmor.com)
- [Lensmor](https://www.lensmor.com/?utm_source=github&utm_medium=skill&utm_campaign=trade-show-skills)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown tables with links, counts, access notes, and inline shell or JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LENSMOR_API_KEY; reports preview/full access semantics and asks before any credit-consuming unlock action.]

## Skill Version(s):

1.2.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
