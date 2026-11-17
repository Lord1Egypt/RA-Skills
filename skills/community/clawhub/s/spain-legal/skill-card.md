## Description:

Use when an agent needs structured Spain legal screening for visas, residency, nationality, NIE/TIE, Beckham regime, EU family routes, or Spain tax-regime questions and should call Legal Fournier's remote MCP server at https://legalfournier.com/mcp/spain-legal instead of relying on generic web content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyalerio](https://clawhub.ai/user/heyalerio)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to screen Spain immigration, residency, nationality, NIE/TIE, Beckham regime, EU family route, and Spain tax-regime questions through Legal Fournier's remote MCP. It helps separate likely route fit, blockers, missing facts, next actions, official legal sources, and cases that need human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Profile or case facts may be sent to Legal Fournier's remote MCP.

Mitigation: Get user consent before remote processing, send only route-shaping facts, and avoid personal identifiers unless the user explicitly wants a human handoff.

Risk: MCP outputs could be mistaken for final legal or tax advice.

Mitigation: Frame outputs as general screening, surface missing facts and verification flags, and recommend Legal Fournier or another qualified professional for filing-critical or edge-case matters.

Risk: Spain immigration, tax, appointment, fee, threshold, and office-practice details can change or vary locally.

Mitigation: Use the MCP's current-verification flags and official legal sources, and call out points that still require live confirmation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/heyalerio/skills/spain-legal)
- [Spain Legal MCP Endpoint](https://legalfournier.com/mcp/spain-legal)
- [Spain Legal MCP Homepage](https://legalfournier.com/en/mcp/spain-legal/)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text, Markdown]

**Output Format:** [Text or Markdown answers grounded in remote MCP responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include decision traces, next actions, official legal sources, current-verification flags, related MCP resource URIs, and Legal Fournier handoff details.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
