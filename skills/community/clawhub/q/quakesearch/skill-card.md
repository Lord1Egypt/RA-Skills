## Description: <br>
Runs Quake CLI asset searches, paginates results, and exports CSV or raw text from search, domain, host, info, and honeypot modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biglizi775](https://clawhub.ai/user/biglizi775) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to run Quake asset-mapping queries through a local Quake CLI binary and collect paginated results for review or follow-up analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a user-provided Quake CLI binary. <br>
Mitigation: Install it only when the agent is expected to run a trusted Quake CLI binary, and verify the binary before use. <br>
Risk: The skill may initialize Quake with a sensitive API key. <br>
Mitigation: Keep the Quake API key in an environment variable such as QUAKE_API_KEY and verify where the Quake CLI stores credentials after initialization. <br>
Risk: CSV or raw output files at selected paths can be overwritten. <br>
Mitigation: Choose output filenames carefully and avoid paths containing existing files that should be preserved. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/biglizi775/quakesearch) <br>
- [Publisher profile](https://clawhub.ai/user/biglizi775) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated runs can write CSV and raw text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Quake CLI binary and may use QUAKE_API_KEY for authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
