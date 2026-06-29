## Description: <br>
Reads current system memory, CPU usage, network throughput, and other real-time performance metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moxin1044](https://clawhub.ai/user/moxin1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support engineers use this skill to inspect local machine performance from an agent session, including CPU, memory, swap, network throughput, disk I/O when available, load averages, process count, and boot time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and displays local machine performance metrics, including CPU, memory, disk I/O, network throughput, process count, and boot time. <br>
Mitigation: Install and run it only in environments where exposing local performance metrics to the active agent session is acceptable. <br>
Risk: The skill depends on psutil for cross-platform system metric collection. <br>
Mitigation: Install psutil from a trusted package source and keep the dependency managed with the surrounding agent environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moxin1044/system-stats) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Plain text performance report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Metrics are sampled locally; CPU, network, and disk rates depend on the sampling interval and platform psutil support.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
