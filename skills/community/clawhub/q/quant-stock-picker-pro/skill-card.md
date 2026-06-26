## Description: <br>
AI-powered stock screening tool for Chinese A-shares. Daily picks using multi-factor analysis (fundamentals + technical + sentiment). Use when user asks about stock screening, quantitative trading, or investment opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ERIC961](https://clawhub.ai/user/ERIC961) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to screen Chinese A-share stocks, generate daily ranked stock-pick reports, and review multi-factor signals, AI model scores, and risk notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that the skill changes network proxy settings and imports code from a hard-coded local path outside the package. <br>
Mitigation: Before running it, remove the hard-coded sys.path entry and remove or make the proxy environment changes explicitly opt-in. <br>
Risk: The skill fetches external market and sentiment data and may be scheduled to run every weekday. <br>
Mitigation: Review the data sources, network access, and schedule before deployment, and choose an output directory appropriate for the local environment. <br>
Risk: Generated stock picks could be mistaken for financial advice. <br>
Mitigation: Treat all recommendations as informational, keep the risk disclosures visible, and require human review before any investment decision. <br>


## Reference(s): <br>
- [Factor Library Documentation](references/factors.md) <br>
- [ClawHub Release Page](https://clawhub.ai/ERIC961/quant-stock-picker-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown stock-screening report with ranked tables and risk notes; scripts may also write CSV output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces informational stock picks and risk disclosures; results should not be treated as investment advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
