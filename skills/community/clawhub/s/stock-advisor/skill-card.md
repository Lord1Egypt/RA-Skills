## Description: <br>
A private AI stock advisor for A-share stock analysis and portfolio management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daasai](https://clawhub.ai/user/daasai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and investors use this skill to request A-share stock analysis reports and manage local portfolio records through agent-run commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The backend API endpoint may receive stock symbols and API credentials during analysis requests. <br>
Mitigation: Set STOCK_ADVISOR_API_URL only to a trusted backend and avoid using a real API key until the provider's data handling is clear. <br>
Risk: The documented curl-to-shell installation step can execute remote installer code. <br>
Mitigation: Use a verified installation method for uv instead of piping a downloaded script directly to a shell. <br>
Risk: The bundled portfolio sample contains local holding data. <br>
Mitigation: Clear data/portfolio.json before using portfolio features with personal holdings. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/daasai/stock-advisor) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stock analysis output may depend on a configured backend API and local portfolio data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
