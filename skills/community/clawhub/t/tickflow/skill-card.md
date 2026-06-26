## Description: <br>
Uses the TickFlow Python SDK to retrieve real-time quotes, historical K-line data, and financial data for A-shares, Hong Kong stocks, U.S. stocks, and futures markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tickflow-dev](https://clawhub.ai/user/tickflow-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to configure TickFlow SDK access and generate Python examples for retrieving market quotes, K-line history, instrument metadata, and financial data across supported equity and futures markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup instructions include a shortcut that pipes the uv installer from astral.sh into the shell or PowerShell. <br>
Mitigation: Prefer installing uv through a trusted package manager when available, or download and inspect the installer before executing it. <br>
Risk: Full TickFlow access depends on an API key stored in the TICKFLOW_API_KEY environment variable. <br>
Mitigation: Handle the API key as a normal runtime credential and avoid placing it in scripts, logs, or committed files. <br>


## Reference(s): <br>
- [TickFlow homepage](https://tickflow.org) <br>
- [ClawHub skill page](https://clawhub.ai/tickflow-dev/tickflow) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, uv, and TICKFLOW_API_KEY for full real-time data access.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
