## Description: <br>
Measure internet network speed, including download, upload, and ping, using speedtest-cli for Speedtest.net. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elony-7](https://clawhub.ai/user/elony-7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run an on-demand Speedtest.net connection check from the host and collect ping, download, upload, and optional server, ISP, and IP details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a live external Speedtest.net network test that can consume bandwidth and disclose network details to the selected test service. <br>
Mitigation: Run it only on networks where external speed-test traffic, bandwidth use, and reported connection details are acceptable. <br>
Risk: The required speedtest-cli dependency is not bundled with the skill. <br>
Mitigation: Install speedtest-cli manually from setup.md and verify the dependency before running the wrapper. <br>


## Reference(s): <br>
- [Setup - Speedtest.net](setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text speed results or JSON from speedtest-cli; Markdown setup guidance when installation is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a live external network speed test; supports optional server selection and timeout settings.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
