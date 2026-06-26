## Description: <br>
Run commands and transfer files between an OpenClaw gateway and a paired local node via node protocol or SSH fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkfaris94](https://clawhub.ai/user/jkfaris94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run commands, transfer files, check node status, and recover from disconnects for an already paired OpenClaw node. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands and file transfers can affect a paired remote node or move unintended files. <br>
Mitigation: Confirm the node target or SSH alias before use, review commands and paths carefully, and use least-privilege SSH accounts. <br>
Risk: Long-running nohup or tmux sessions can continue after the initiating agent session ends. <br>
Mitigation: Use explicit process names, log paths, and follow-up status checks so work can be monitored and stopped when needed. <br>
Risk: SSH fallback depends on network reachability and correct local SSH configuration. <br>
Mitigation: Check node status first, verify SSH reachability with a harmless command, and recover the paired node service only through the remote machine's normal service manager. <br>


## Reference(s): <br>
- [Remote Node SSH homepage](https://github.com/kanso-agent/remote-node-ssh) <br>
- [Hybrid Gateway setup skill](https://clawhub.ai/skills/hybrid-gateway) <br>
- [ClawHub release page](https://clawhub.ai/jkfaris94/remote-node-ssh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline tool and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
