## Description: <br>
Monitors ValueScan stream events for market analysis and token signals, then persists received data to local files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[valuescan-io](https://clawhub.ai/user/valuescan-io) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and crypto operations users use this skill to configure and run background monitoring for ValueScan market analysis and token signal streams, writing the resulting events into local files for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores ValueScan API credentials in plaintext under ~/.vs-monitor/config.json. <br>
Mitigation: Use a dedicated low-privilege account or container, create a dedicated ValueScan API key, and restrict filesystem permissions on ~/.vs-monitor and config.json. <br>
Risk: Persistent monitor processes are managed through PID files and may terminate existing processes. <br>
Mitigation: Review process management before use and verify PIDs before stopping processes. <br>
Risk: Output file paths can be built from streamed token data. <br>
Mitigation: Choose a non-sensitive output directory and require maintainer-side sanitization and output-path containment. <br>


## Reference(s): <br>
- [ValueScan homepage](https://www.valuescan.ai) <br>
- [ValueScan stream API reference](references/stream-api.json) <br>
- [ClawHub skill page](https://clawhub.ai/valuescan-io/valuescan-monitor-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; runtime monitoring appends plain text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ValueScan API credentials, starts persistent monitor processes, and writes market analysis and token signal events under a user-selected output directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
