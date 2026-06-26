## Description: <br>
Proxmox VE VM builder with cloud-init automation, config-driven hardware defaults, validation, and static IP support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mbojer](https://clawhub.ai/user/mbojer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to prepare Proxmox VE VM creation guidance, including cloud-init setup, SSH key handling, network configuration, storage choices, and copyable qm commands for manual execution on a Proxmox node. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bootstrap VM passwords may be exposed in chat transcripts or generated command files. <br>
Mitigation: Prefer SSH-key-only provisioning when possible, avoid saving passwords in generated files, and rotate any bootstrap password immediately after first access. <br>
Risk: The skill uses local shell execution and writes SSH key material, so broad permissions can affect the local environment. <br>
Mitigation: Use a dedicated locked-down SSH key directory, review generated shell and Proxmox commands before running them, and keep private key files permissioned to the local user. <br>
Risk: Software requirement lookups can disclose internal product names, URLs, or deployment context. <br>
Mitigation: Avoid sensitive internal URLs or names in web lookups and provide manual sizing inputs when the workload details are confidential. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mbojer/pve-builder) <br>
- [Proxmox QM Command Reference](artifact/qm-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces commands for the user to review and run manually on a Proxmox node; it does not verify VM creation itself.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata; artifact frontmatter reports 1.0.10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
