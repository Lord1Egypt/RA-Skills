## Description: <br>
Quick Resurrection packages and restores OpenClaw Agent workspace configuration so users can migrate an agent team after changing machines or reinstalling an environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhao-zwl](https://clawhub.ai/user/zhao-zwl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw Agent users and developers use this skill to package an existing agent workspace, transfer it to a new environment, restore agent configuration, and optionally recreate scheduled tasks after reviewing the planned changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can package private agent data such as memories, tool configuration, and credentials into migration archives. <br>
Mitigation: Run the migration in dry-run mode first, inspect MEMORY.md, TOOLS.md, included skills, and generated archives, and keep archives encrypted or otherwise protected. <br>
Risk: The skill can restore persistent cron tasks and OpenClaw configuration in the target environment. <br>
Mitigation: Review the full cron payloads and openclaw-agents.json before confirming, and use --no-cron for the first run when scheduled task restoration is not needed. <br>
Risk: The skill can restart the OpenClaw gateway and change runtime behavior after migration. <br>
Mitigation: Use --no-restart during initial review, verify the merged configuration, and restart manually after confirming the target environment is correct. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhao-zwl/quick-resurrection) <br>
- [README](artifact/README.md) <br>
- [Material Packing Guide](artifact/MATERIAL_PACKING.md) <br>
- [Usage Examples](artifact/examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated configuration files, and migration archive artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May package sensitive workspace files and may restore OpenClaw configuration and cron task definitions after user confirmation.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
