## Description: <br>
Save stock investment strategies with entry and exit conditions in a local Markdown file, then check current market data to recommend next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dcsight](https://clawhub.ai/user/dcsight) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to persist stock strategy notes, compare entry and exit conditions against current market data, and produce action-oriented review summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The save workflow can create or overwrite the configured Markdown tracking file. <br>
Mitigation: Use a dedicated STOCK_SCHEME_PATH file, ideally under the user's home directory, and avoid pointing it at unrelated Markdown documents. <br>
Risk: Check mode may query external finance or web tools for market data. <br>
Mitigation: Limit external queries to public ticker symbols and metric names, and do not send saved strategy details or private position information. <br>
Risk: Generated recommendations can be outdated or misleading if market data or saved assumptions are stale. <br>
Mitigation: Review recommendations against current market data before acting; the skill provides analysis only and does not execute trades. <br>


## Reference(s): <br>
- [Scheme Format Reference](references/scheme_format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and local Markdown file entries, with JSON used for script input and parsed strategy data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses STOCK_SCHEME_PATH to select the local tracking file; check mode may rely on agent-provided finance or web tools for public market data.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
