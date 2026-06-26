## Description: <br>
Wyckoff Screen scans China A-share market data for stocks that appear to be in late accumulation or early trend-start phases, then returns ranked candidates with scoring and workflow notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxarch1980](https://clawhub.ai/user/dxarch1980) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run post-close stock screening over China A-share data with Wyckoff phase and volume-profile scoring. It helps produce a ranked candidate list, supporting signals, and workflow notes for further human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports an embedded market-data credential. <br>
Mitigation: Remove the embedded credential, rotate it, and require users to provide their own credential through configuration or a secret store. <br>
Risk: The security summary reports authenticated requests to an undisclosed plain-HTTP IP endpoint. <br>
Mitigation: Use a documented HTTPS endpoint where possible, or clearly document and justify the endpoint before installation. <br>
Risk: The security guidance calls for confirmation and configuration around broad scans and local persistence. <br>
Mitigation: Require explicit user confirmation for broad market scans and document the local SQLite files written by the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dxarch1980/wyckoff-screen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets; runtime output is terminal text and saved .txt screening reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs ranked candidate stocks with code, phase, VPOC, current price, signals, and score; default runtime output is limited to top 20 candidates.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
