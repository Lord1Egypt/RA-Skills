## Description: <br>
A clean, reliable system resource monitor for CPU load, RAM, swap, disk usage, and uptime, optimized for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nguyenttham085](https://clawhub.ai/user/nguyenttham085) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to request concise server health reports for an OpenClaw host, including CPU load, memory, swap, root disk usage, and uptime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor sends uptime, load, memory, swap, and disk usage to a fixed external webhook every time it runs. <br>
Mitigation: Review the script before installation and remove or disable the curl POST unless remote reporting to that endpoint is explicitly approved. <br>
Risk: The reporting endpoint is hard-coded, so users cannot choose or audit the destination at runtime. <br>
Mitigation: Make remote reporting opt-in and require a user-controlled endpoint before running the skill in an operational environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nguyenttham085/test-monitor-openclaw-server) <br>
- [Publisher profile](https://clawhub.ai/user/nguyenttham085) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text server resource report with shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local shell script and may send collected host resource data to a fixed external webhook.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
