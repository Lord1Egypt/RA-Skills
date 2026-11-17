## Description:

Performs systematic investment-value analysis for listed companies, including fundamentals, technical indicators, valuation, peer comparison, and HTML/PDF-style report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newhackerman](https://clawhub.ai/user/newhackerman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to gather public market data, evaluate A-share, Hong Kong, and U.S. listed companies, compare peers, and produce structured investment-analysis reports. Outputs are informational and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that generated reports may be served through an unauthenticated local web server on port 8888.

Mitigation: Run report generation only in a contained environment, avoid exposing port 8888, and stop the server after use.

Risk: The security scan reports that user-derived report filenames are written without adequate safety controls.

Mitigation: Use trusted stock codes and company names, validate or sanitize inputs before routine use, and review generated file paths.

Risk: The security guidance flags input validation, HTML escaping, HTTPS-only data sources, and server cleanup as areas to fix before routine use.

Mitigation: Review and harden these areas before installing the skill for regular or shared-environment use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/newhackerman/skills/stock-analysis-best)
- [Valuation methods reference](artifact/references/valuation-methods.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown, terminal output, and generated HTML reports with browser print-to-PDF guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public market data, writes cached data and report files, and may print local report access instructions.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
