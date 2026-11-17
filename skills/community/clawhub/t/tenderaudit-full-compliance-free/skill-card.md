## Description:

TenderAudit Full Compliance (Free) locally checks bidding-document inputs for per-bidder quote arithmetic errors and unreplaced template placeholders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement, bid, and operations teams use this skill before submission to run a local pre-check of bidder quote line arithmetic and leftover template placeholders. It is a pre-screen, not a legal opinion or official bid-evaluation decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender files may contain sensitive bid, pricing, or supplier information.

Mitigation: Run the checker only on files the user is comfortable processing locally; the security evidence reports no network use or persistence.

Risk: The output may be mistaken for an official legal, scoring, or bid-evaluation decision.

Mitigation: Treat findings as a mechanical pre-check only and route final decisions to the responsible procurement, legal, or evaluation authority.

Risk: The free version covers only quote arithmetic and template-placeholder scanning.

Mitigation: Review the reported withheld checks before relying on the result, especially for tender-document substance, contract terms, collusion indicators, or final remediation planning.

Risk: Incomplete or malformed input can produce no checkable result for some bidders.

Mitigation: Provide a bidders array with each bidder's structured items and/or text; treat NOT_CHECKED or insufficient-input responses as missing evidence, not as clean results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/tenderaudit-full-compliance-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON command output containing checks performed, per-bidder findings, risk summaries, missing-input guidance, and withheld checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided JSON; normal execution exits 0, insufficient input exits 3, and unreadable input exits 4.]

## Skill Version(s):

1.1.43 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
