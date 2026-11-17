## Description:

Negotiation math engine for Pareto frontier analysis, iso-utility counteroffer generation, and preference inference via MILP optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rjandino](https://clawhub.ai/user/rjandino)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and negotiation-support workflows use this skill to model multi-issue negotiations, analyze deal quality, generate multiple counteroffer packages, and infer counterpart priorities from responses. Common scenarios include job offers, VC term sheets, real estate, vendor contracts, partnerships, procurement, and legal settlements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured hosted MCP service may receive sensitive negotiation details such as deal terms, BATNA information, salary walk-away positions, private term sheets, or vendor pricing.

Mitigation: Use the hosted endpoint only after confirming the operator's retention, access-control, and third-party model-use policies, or configure a local/on-prem server for confidential negotiations.

Risk: The security summary notes broader session, persistence, and LLM-backed web-coach code that is not clearly disclosed in the skill description.

Mitigation: Review the release before installation and limit deployment to the MCP behavior and hosting model that match the intended risk posture.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rjandino/skills/zopaf)
- [Configured Zopaf MCP endpoint](https://zopaf-mcp-production.up.railway.app/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and text guidance with MCP tool calls, JSON-like tool responses, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces negotiation sessions, issue models, preference weights, BATNA summaries, counteroffer packages, deal analyses, and next-step recommendations.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
