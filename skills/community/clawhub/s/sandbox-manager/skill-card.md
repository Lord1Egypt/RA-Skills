## Description: <br>
Creates and manages Baidu Agent Sandbox instances, including setup, connection, command execution, file listing, and teardown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igogo888](https://clawhub.ai/user/igogo888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to provision, connect to, inspect, run commands in, and destroy Baidu Agent Sandbox environments through an agent or command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sandbox credentials may be written to ~/.env and partially echoed in logs. <br>
Mitigation: Review credential writes before installation, prefer session-only environment variables or a restricted credential file, and rotate the API key if it appears in logs or screenshots. <br>
Risk: The skill can execute commands inside sandbox instances and destroy sandbox resources. <br>
Mitigation: Confirm command execution and sandbox deletion explicitly, and avoid sharing sandbox URLs or identifiers outside trusted channels. <br>
Risk: The skill depends on a Baidu sandbox service and package index. <br>
Mitigation: Install only when the Baidu service and package index are trusted for the intended environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/igogo888/sandbox-manager) <br>
- [Baidu sandbox management platform](https://console.cloud.baidu-int.com/aitools/sandbox-square) <br>
- [Baidu sandbox usage documentation](https://ku.baidu-int.com/knowledge/HFVrC7hq1Q/_SKPgSwp2G/B8wSneaLSC/xBjsa6yz-ZsV4-) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and Python snippets plus command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return sandbox identifiers, service URLs, command output, and configuration steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
