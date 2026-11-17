## Description:

Southwest Florida real-estate and local-economy data for Lee and Collier County home prices, days on market, inventory, ZIP-level reports, flood and insurance exposure, and permit context, with sourced and dated figures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ethanrickyjrjr-wq](https://clawhub.ai/user/ethanrickyjrjr-wq)

### License/Terms of Use:

MIT-0

## Use Case:

External users, agents, and developers use this skill to answer Southwest Florida housing, ZIP-level market, flood/insurance, permit, CRE, and local economic questions using public SWFL Data Gulf data. It is intended for sourced market lookups and analysis, not for named-business, street-address, purchase, or authenticated account workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent may present time-sensitive market figures without their source, as-of date, freshness date, or caveats.

Mitigation: Preserve the source labels, dates, freshness statements, and caveats returned by SWFL Data Gulf when relaying figures.

Risk: Repeated public endpoint calls can hit the observed 60 requests per minute rate limit.

Mitigation: Use targeted requests and space out loops or repeated curl calls.

Risk: Users may ask the agent to authenticate, purchase a plan, or send content under a human account.

Mitigation: Keep the skill to public unauthenticated reads and direct humans to the billing page for account or purchase actions.

## Reference(s):

- [SWFL Data Gulf homepage](https://www.swfldatagulf.com)
- [Agent site map](https://www.swfldatagulf.com/llms.txt)
- [Housing SWFL speak digest endpoint](https://www.swfldatagulf.com/api/b/housing-swfl?view=speak&tier=2&v=5)
- [Master speak digest endpoint](https://www.swfldatagulf.com/api/b/master?view=speak&tier=2&v=5)
- [SWFL Data Gulf MCP endpoint](https://www.swfldatagulf.com/api/mcp)
- [Skill page on ClawHub](https://clawhub.ai/ethanrickyjrjr-wq/skills/swfl-data-gulf)
- [Publisher profile on ClawHub](https://clawhub.ai/user/ethanrickyjrjr-wq)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with curl commands, endpoint references, citation instructions, and optional MCP configuration notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should preserve each returned figure's stated source, as-of date, freshness date, and caveats.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
