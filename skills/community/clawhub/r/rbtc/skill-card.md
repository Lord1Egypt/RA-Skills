## Description: <br>
Runs a patched Bitcoin Core node with built-in CPU mining, configurable CPU usage, verification workflows, and update commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happybigmtn](https://clawhub.ai/user/happybigmtn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to install, verify, build, run, mine with, and update an rBitcoin node derived from Bitcoin Core. It is intended for users who understand local compilation, node operation, RPC exposure, and CPU mining resource costs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default quickstart can start CPU mining and consume sustained CPU, power, and disk resources. <br>
Mitigation: Set START_MINER=0 for install or verification unless mining is explicitly intended, and cap mining with MINER_CPU_PERCENT and MINER_MAX_THREADS. <br>
Risk: The package points to install and helper scripts that are not bundled in the artifact reviewed here. <br>
Mitigation: Review the source repository and exact install.sh and scripts before executing them. <br>
Risk: Node and miner workflows may perform network activity and expose RPC configuration choices. <br>
Mitigation: Keep RPC_BIND and RPC_ALLOWIP restricted to localhost unless a reviewed deployment plan requires broader access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/happybigmtn/rbtc) <br>
- [Project homepage from artifact metadata](https://github.com/happybigmtn/rBTC) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON reports] <br>
**Output Format:** [Markdown with bash commands, environment variable settings, and generated verification report paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may trigger local compilation, network access, disk usage, and sustained CPU mining load.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
