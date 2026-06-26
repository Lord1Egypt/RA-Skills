## Description: <br>
Provides structured Spain legal screening for visas, residency, nationality, NIE/TIE, Beckham regime, EU family routes, and Spain tax-regime questions through Legal Fournier's remote MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heyalerio](https://clawhub.ai/user/heyalerio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to screen Spain immigration, residency, nationality, NIE/TIE, Beckham regime, EU family, and Spain tax-regime questions through Legal Fournier's MCP while preserving consent and data minimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Case facts may be sent to Legal Fournier's remote MCP service. <br>
Mitigation: Get user consent before remote processing, minimize facts sent, and avoid personal identifiers or documents unless the user knowingly requests a handoff. <br>
Risk: Screening output could be mistaken for final legal or tax advice. <br>
Mitigation: Frame results as informational screening and recommend lawyer or professional review for filing-critical, sensitive, or edge-case matters. <br>
Risk: Spain appointment availability, fees, thresholds, and office practice can change. <br>
Mitigation: Use MCP current-verification flags, avoid inventing volatile details, and state what still needs live confirmation. <br>


## Reference(s): <br>
- [Spain Legal MCP endpoint](https://legalfournier.com/mcp/spain-legal) <br>
- [Spain Legal MCP homepage](https://legalfournier.com/en/mcp/spain-legal/) <br>
- [ClawHub skill page](https://clawhub.ai/heyalerio/spain-legal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance based on structured MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include decision traces, next actions, official source references, verification flags, and Legal Fournier handoff details when returned by the MCP.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
