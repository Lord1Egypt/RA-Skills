## Description:

Searches PatSnap's TRIZ case library through a hosted MCP endpoint to find analogous technical cases, cross-domain solution patterns, applied invention principles, and scientific effects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwt1995](https://clawhub.ai/user/wwt1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical researchers use this skill to search for patent-backed analogous cases and TRIZ solution patterns for engineering problems, physical contradictions, cross-domain inspiration, and prior-art exploration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search criteria and technical problem descriptions to PatSnap/Eureka RD.

Mitigation: Redact confidential inventions, trade secrets, personal data, NDA-protected details, proprietary technology, and export-controlled content before use.

Risk: Analogous case-search results may be mistaken for proof of engineering feasibility, freedom to operate, absence of patent risk, or legal advice.

Mitigation: Use results as inspiration only, validate technical applicability independently, and route patent or legal questions to qualified reviewers.

Risk: The skill depends on an external hosted endpoint and HTTP helper behavior that can fail, time out, or change schema.

Mitigation: Inspect the live tool definitions when calls fail, report actual HTTP or JSON-RPC errors, and avoid guessing unsupported parameters.

Risk: The skill appends a promotional Eureka RD link after results once per session.

Mitigation: Treat the link as a disclosed product call-to-action and avoid presenting it as part of the case-search evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwt1995/skills/solution-case-finder)
- [Eureka RD](https://eureka.patsnap.com/rd/#/agentic?type=triz&start_from=clawhub&utm_source=clawhub&utm_medium=skill_listing&utm_campaign=triz_case_finder)
- [PatSnap TRIZ case library MCP endpoint](https://ai-fabric.patsnap.com/mcp/patsnap-triz-case-library?APP_ID=Patsnap)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with JSON examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ranked case-search summaries, transferable solution insights, limitations, validation guidance, and optional JSON results from the HTTP helper.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
