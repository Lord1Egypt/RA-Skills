## Description: <br>
Query Dutch Railways (NS) for train departures, trip planning, disruptions, and station search via the trein CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Joehoel](https://clawhub.ai/user/Joehoel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for Dutch Railways CLI commands and setup guidance for real-time departures, trip planning, disruptions, station search, aliases, and structured JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires installing and running the third-party trein CLI. <br>
Mitigation: Install only from the package or release locations named in the evidence, and review the CLI before using it in sensitive environments. <br>
Risk: The skill requires an NS_API_KEY and can store it in a local configuration file. <br>
Mitigation: Provide the key through a secret-aware environment variable when possible, and treat ~/.config/trein/trein.config.json as a secret-bearing file if used. <br>


## Reference(s): <br>
- [NS API Portal](https://apiportal.ns.nl/) <br>
- [trein macOS Apple Silicon binary](https://github.com/joelkuijper/trein/releases/latest/download/trein-darwin-arm64) <br>
- [trein macOS Intel binary](https://github.com/joelkuijper/trein/releases/latest/download/trein-darwin-x64) <br>
- [trein Linux x64 binary](https://github.com/joelkuijper/trein/releases/latest/download/trein-linux-x64) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide use of the trein CLI --json flag for structured command output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
