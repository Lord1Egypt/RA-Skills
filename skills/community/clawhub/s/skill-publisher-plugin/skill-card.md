## Description: <br>
Helps agents publish local skills to the ClawHub marketplace by checking login state, inspecting existing releases, and proposing publish or update commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vivian8725118](https://clawhub.ai/user/vivian8725118) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this agent skill to prepare ClawHub publish commands, choose initial or update versioning, and publish local skill directories to the marketplace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publish commands can make local skill content public on ClawHub. <br>
Mitigation: Require explicit user confirmation of the target directory, slug, version, and account before running any publish command. <br>
Risk: A local skill may contain secrets, proprietary content, or files that should not be published. <br>
Mitigation: Inspect the files for secrets or proprietary content before publishing. <br>
Risk: Loose activation could lead an agent to prepare publishing actions when the user did not intend a public release. <br>
Mitigation: Use the skill only when the user clearly asks to publish or update a ClawHub skill. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/vivian8725118/skill-publisher-plugin) <br>
- [Publisher profile](https://clawhub.ai/user/vivian8725118) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ClawHub CLI commands for login checks, release inspection, publishing, syncing, semantic version choices, and changelog text.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
