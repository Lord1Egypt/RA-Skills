## Description: <br>
Helps developers install, configure, run, troubleshoot, and extend MolecularAI REINVENT4 workflows for generative molecular design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoeprior](https://clawhub.ai/user/zoeprior) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, computational chemistry teams, and coding agents use this skill to work through REINVENT4 installation, backend selection, TOML configuration, runtime commands, troubleshooting, plugin setup, notebook conversion, and tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated install, run, or configuration commands may change a local Python environment or development workspace. <br>
Mitigation: Use the skill only in a trusted workspace, review commands before execution, and prefer help or dry-run commands when backend choice or dependency resolution is uncertain. <br>
Risk: Full REINVENT4 workflows may depend on local models, datasets, hardware backends, or optional licensed tools that are not present. <br>
Mitigation: Verify required files, device settings, writable outputs, and optional license availability before running full workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoeprior/reinvent4) <br>
- [Install and run guidance](artifact/references/install-and-run.md) <br>
- [Configuration modes guidance](artifact/references/config-modes.md) <br>
- [Plugins, notebooks, and tests guidance](artifact/references/plugins-and-tests.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, TOML configuration guidance, and code-oriented examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Grounds recommendations in a local REINVENT4 checkout and upstream reference files when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
