## Description:

Qinghu AI 1688 Sourcing helps ecommerce sellers search 1688 suppliers by image, keyword, or product detail lookup, then compare prices, minimum order quantities, supplier signals, and sourcing costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers and sourcing agents use this skill to find same-style products on 1688, compare supplier offers, and estimate procurement costs before deciding what to source. It supports sourcing evaluation and does not handle ordering, negotiation, or logistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use a Qinghu API token.

Mitigation: Use a dedicated Qinghu API key and avoid exposing the token in chat or exported artifacts.

Risk: Approved Qinghu API calls may consume paid credits.

Mitigation: Ask for user authorization before calls, report actual consumption from the returned pointCost value, and avoid unnecessary retries.

Risk: Larger result sets may be exported to local spreadsheet files.

Mitigation: Share the generated file path with the user and handle exported supplier data according to the user's local data policy.

Risk: 1688 same-style matches and supplier listings may not guarantee identical quality, favorable minimum order quantities, or acceptable fulfillment timing.

Mitigation: Compare multiple suppliers, call out assumptions, and recommend sample checks before the user commits to sourcing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-1688-sourcing)
- [Qinghu data API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown responses with supplier comparisons, concise recommendations, JSON request examples, and local spreadsheet files for larger result sets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user authorization before Qinghu API calls; larger result sets are exported instead of pasted into chat.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
