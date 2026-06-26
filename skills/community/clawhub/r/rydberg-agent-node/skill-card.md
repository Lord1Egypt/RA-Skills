## Description: <br>
Deploys and manages a ProbeChain Rydberg testnet Agent node, including installation, startup, status checks, logs, balance checks, and Agent registration commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ProbeBuilders](https://clawhub.ai/user/ProbeBuilders) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and node operators use this skill to install, start, monitor, and manage a local ProbeChain Rydberg testnet Agent node across macOS, Linux, and Windows via WSL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads or builds node software and starts a long-running local background process. <br>
Mitigation: Review the GitHub source or release being used, run it only on machines intended for a ProbeChain Rydberg Agent testnet node, and monitor ~/rydberg-agent/node.log. <br>
Risk: The skill stores a local node password and unlocks the node account through local IPC. <br>
Mitigation: Use a unique node password, keep generated files private, and avoid exposing sensitive admin or personal APIs over HTTP. <br>
Risk: The skill writes blockchain data, logs, scripts, and credentials under ~/rydberg-agent. <br>
Mitigation: Review generated files, keep filesystem permissions restricted, and stop the node process before removing local node data. <br>
Risk: The skill uses outbound network access for release downloads, source builds, genesis data, and bootnode connectivity. <br>
Mitigation: Run it only on networks where that access is expected and verify release checksums or signatures when they are available. <br>


## Reference(s): <br>
- [ProbeChain homepage](https://probechain.org) <br>
- [ProbeChain Rydberg repository](https://github.com/ProbeChain/Rydberg-Mainnet) <br>
- [Rydberg Agent Node on ClawHub](https://clawhub.ai/ProbeBuilders/rydberg-agent-node) <br>
- [Go downloads](https://go.dev/dl/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with shell command blocks and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces install, start, stop, status, log, balance, and re-registration guidance; may request a local node password.] <br>

## Skill Version(s): <br>
2.5.1 (source: server release metadata; artifact frontmatter reports 2.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
