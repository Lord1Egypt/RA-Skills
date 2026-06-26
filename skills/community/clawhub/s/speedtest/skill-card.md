## Description: <br>
Test internet connection speed using Ookla's Speedtest CLI, measure download and upload speeds, latency, and packet loss, format results for Moltbook or Twitter sharing, and track speed history over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spsneo](https://clawhub.ai/user/spsneo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to run internet speed tests, inspect connection quality, save local speed history, and optionally format or publish network-performance results to social platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill combines speed testing with optional credential-backed social posting. <br>
Mitigation: Enable posting only when the user is comfortable with the skill reading configured credentials and publishing network-performance results externally. <br>
Risk: Installation guidance includes curl-to-sudo package repository setup. <br>
Mitigation: Review and verify the installer source before running elevated install commands. <br>
Risk: Speed-test results are written to a local history file. <br>
Mitigation: Review the history path and contents before using the skill in environments where network-performance data is sensitive. <br>


## Reference(s): <br>
- [Speedtest CLI Reference](references/speedtest-cli.md) <br>
- [Ookla Speedtest CLI](https://www.speedtest.net/apps/cli) <br>
- [ClawHub Speedtest Skill](https://clawhub.ai/spsneo/speedtest) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, generated social-post text, and local JSON Lines history records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run external speed tests, write local history under ~/.openclaw/data, and optionally publish results to Moltbook or Twitter when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
