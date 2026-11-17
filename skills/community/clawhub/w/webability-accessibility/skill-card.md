## Description:

Scan pages and HTML for WCAG 2.2, ADA and Section 508 accessibility issues with the WebAbility MCP server, get framework-aware fixes, and verify each fix with a re-scan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snayyar00](https://clawhub.ai/user/snayyar00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan web pages, components, or HTML for accessibility issues, apply framework-aware fixes, and check results with a follow-up scan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted scans send submitted URLs and HTML to WebAbility.

Mitigation: Remove secrets and confirm private content may be shared before submitting URLs or HTML.

Risk: Generated accessibility fixes may be incorrect or incomplete.

Mitigation: Review proposed changes, then re-scan and report verification only when the tool confirms it.

Risk: Optional local execution installs software and may access local files.

Mitigation: Pin a reviewed package version or image digest and limit filesystem access.

## Reference(s):

- [WebAbility MCP documentation](https://www.webability.io/mcp)
- [WebAbility](https://www.webability.io/)
- [ClawHub release page](https://clawhub.ai/snayyar00/skills/webability-accessibility)

## Skill Output:

**Output Type(s):** [Text, Code, Guidance]

**Output Format:** [Accessibility findings, framework-aware code suggestions, and scan verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results reflect the selected scan tools; automated scans do not establish full accessibility conformance.]

## Skill Version(s):

1.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
