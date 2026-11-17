## Description:

Substantiates an EU ebook accessibility claim for the release EPUB before approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powmcp](https://clawhub.ai/user/powmcp)

### License/Terms of Use:

MIT-0

## Use Case:

External publishing, production, and accessibility teams use this skill to check a release EPUB or compare revised builds before approving EU accessibility claims and ONIX accessibility metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured remote PowMCP MCP service can receive complete EPUB files during checks.

Mitigation: Use the documented local DAISY Ace path for confidential, embargoed, unpublished, or otherwise sensitive EPUBs unless external service use is approved.

Risk: The release evidence flags mutable installation through an npx command.

Mitigation: Prefer a pinned or verified installer or source revision before deployment.

Risk: The MCP dependency allows implicit invocation in supported clients.

Mitigation: Review which EPUB is being sent before invocation and avoid authenticated URLs, credentials, or query strings in check inputs.

Risk: Automated DAISY Ace results do not establish full accessibility, WCAG conformance, EPUB Accessibility 1.1 conformance, or legal compliance.

Mitigation: Pair the automated evidence with separate EPUBCheck structural validation, qualified manual accessibility review, DRM obstruction review, and ONIX reconciliation before approval.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/powmcp/skills/substantiate-eu-ebook-accessibility-claim)
- [Ebook Accessibility Check reference](artifact/references/epub-accessibility-check.md)
- [PowMCP Ebook Accessibility Check app](https://powmcp.com/apps/epub-accessibility-check/)
- [DAISY ONIX accessibility metadata guidance](https://kb.daisy.org/publishing/docs/metadata/onix/)
- [W3C accessibility metadata crosswalk](https://w3c.github.io/a11y-discov-vocab/crosswalk/)
- [AccessibilitySummary authoring guidelines](https://github.com/benetech/AccessibilitySummaryEPUBMetadata/blob/master/AccessibilitySummaryAuthoringGuidelines.md)
- [EDItEUR accessibility metadata in ONIX application note](https://www.editeur.org/files/ONIX%203/APPNOTE%20Accessibility%20metadata%20in%20ONIX.pdf)
- [European Accessibility Act ebook checklist](https://publica.la/en/blog/european-accessibility-act-checklist-ebook-store-compliant)
- [PowMCP Ebook File Check](https://powmcp.com/apps/epub-check/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown evidence reports and concise prose with command snippets when connection or local fallback steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exact tool-returned values, risk boundaries, not-checked items, and approval handoff language.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
