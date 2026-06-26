## Description: <br>
Queries alternative financial data from Quiver Quantitative, including Congress trading, lobbying, government contracts, and insider transactions, to help track unconventional market signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stuhorsman](https://clawhub.ai/user/stuhorsman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, analysts, and developers use this skill to run Quiver Quantitative API queries for alternative financial datasets such as congressional trades, lobbying spend, government contracts, and insider transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Quiver Quantitative API key and calls an external financial-data API. <br>
Mitigation: Provide the key only through a controlled QUIVER_API_KEY environment variable and install the quiverquant Python package from a trusted source. <br>
Risk: The skill returns alternative financial data that may require review before operational or investment use. <br>
Mitigation: Treat returned JSON as source data for further analysis and corroborate it with other trusted sources before acting on it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/stuhorsman/quiver) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown usage guidance with command output as JSON arrays] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QUIVER_API_KEY and the quiverquant Python package; returned records depend on Quiver Quantitative API access.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
