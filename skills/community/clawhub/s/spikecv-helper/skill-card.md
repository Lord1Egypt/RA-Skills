## Description:

Help AI agents answer questions and execute tasks for SpikeCV, an ultra-high-speed spike camera vision framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhs183019](https://clawhub.ai/user/lhs183019)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get SpikeCV setup guidance, navigate the SpikeCV project, download spike-camera datasets, and run supported SpikeCV CLI workflows for reconstruction and tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and dataset workflow commands can download files, install packages, or change the user's shell environment.

Mitigation: Review commands before execution, use a virtual environment or container, and confirm dataset downloads and conda init profile changes are acceptable.

Risk: Following the latest SpikeCV repository state may introduce unreviewed upstream changes.

Mitigation: Pin the SpikeCV repository to a reviewed commit when repeatability or security review is required.

Risk: Miniconda installer commands download executable installers from the network.

Mitigation: Verify installers where possible and use trusted network and package sources.

## Reference(s):

- [About SpikeCV](references/About_SpikeCV.md)
- [Install Miniconda](references/install_miniconda.md)
- [SpikeCV Documentation](https://spikecv.readthedocs.io)
- [SpikeCV Official Website](https://spikecv.github.io)
- [SpikeCV Publications](https://spikecv.github.io/publications.html)
- [SpikeCV: open a continuous computer vision era](https://link.springer.com/article/10.1007/s11432-023-4565-6)
- [SpikeCV Code Repository](https://github.com/Zyj061/SpikeCV)
- [SpikeCV OpenI Datasets](https://openi.pcl.ac.cn/Cordium/SpikeCV/datasets)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI-oriented troubleshooting notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends structured SpikeCV CLI output with --agent-used when supported.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
