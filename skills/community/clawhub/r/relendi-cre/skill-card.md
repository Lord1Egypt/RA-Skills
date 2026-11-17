## Description:

Use Relendi's public CRE loan calculators when the user asks to size a commercial mortgage, stress-test DSCR, compare loan terms, estimate NY/FL closing costs, or save a financing scenario to Relendi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[royamir1](https://clawhub.ai/user/royamir1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents supporting commercial real estate financing analysis use this skill to size loans, stress-test DSCR, compare terms, estimate NY/FL closing costs, and prepare optional Relendi deal handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commercial real estate scenario inputs such as NOI, property value, rates, and loan terms are sent to Relendi's public calculators.

Mitigation: Send only the inputs needed for the requested calculation and avoid personal identifiers, bank details, full documents, unrelated confidential material, and full conversation contents.

Risk: A Relendi handoff URL may contain scenario inputs.

Mitigation: Review the URL before sharing it and share it only with intended recipients.

Risk: Calculator results are illustrative and may be mistaken for lender quotes, approvals, or verified property facts.

Mitigation: Label assumptions and limiting factors clearly, and do not present generated limits or handoff links as approvals, applications, saved drafts, or lender actions.

Risk: Different Relendi tools use different rate units.

Mitigation: Inspect and follow the returned tool schema, using decimal rates for sizing, metrics, and payment tools and percent rates for finance and stress tools.

## Reference(s):

- [Relendi MCP](https://relendi.com/mcp)
- [Relendi public MCP endpoint](https://relendi.com/api/mcp/public)
- [Relendi public tools API](https://relendi.com/api/v1/tools)
- [ClawHub skill page](https://clawhub.ai/royamir1/skills/relendi-cre)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional inline shell commands, links, cited explanations, and calculator result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Relendi-returned handoff URLs and cited CRE explanations when the called operation provides them.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
