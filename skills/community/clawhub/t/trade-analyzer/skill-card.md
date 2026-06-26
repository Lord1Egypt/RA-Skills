## Description: <br>
Analyzes user-provided trade records and produces Markdown reports with win rate, profit/loss ratio, strategy consistency, risk indicators, and improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[misso0513](https://clawhub.ai/user/misso0513) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts can use this skill to parse CSV or text trade-history data and generate a structured review of trading performance, behavior patterns, and possible improvements. It is intended for local analysis of user-provided records rather than investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trade-history files may contain account, personal, or sensitive financial details. <br>
Mitigation: Install only if comfortable providing trade-history data for local analysis, redact unnecessary identifiers, and prefer CSV or text inputs. <br>
Risk: Parsed columns or generated statistics can be wrong when the source file uses unexpected headers or formatting. <br>
Mitigation: Review parsed columns and computed results before relying on the report. <br>
Risk: Excel processing is described as dependent on a separate helper rather than implemented directly in the bundled analyzer. <br>
Mitigation: Review any separate Excel-processing helper before using .xlsx files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/misso0513/trade-analyzer) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown report with tables, summary statistics, ASCII charts, and recommendations; Python helper code is included in the artifact.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are based on parsed user-supplied trade records; CSV and text inputs are implemented locally, while Excel support depends on a separate helper.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
