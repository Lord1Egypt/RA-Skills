## Description: <br>
Skill Publish Tool automates version updates, changelog edits, Git commits and pushes, and ClawHub publishing for OpenClaw skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shinelp100](https://clawhub.ai/user/shinelp100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to publish OpenClaw skill updates by preparing version metadata, changelog entries, Git changes, and ClawHub release commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change local files, update release metadata, commit changes, push to the configured Git remote, and publish to ClawHub. <br>
Mitigation: Review the target skill path, generated diffs, Git remote, version, and changelog before allowing publish steps to run. <br>
Risk: The security evidence flags an unsafe shell-command pattern and warns against untrusted changelog or commit text. <br>
Mitigation: Use trusted changelog text, avoid shell metacharacters in user-provided values, and prefer manual review or skip flags for sensitive repositories. <br>
Risk: The artifact documentation includes force-push troubleshooting guidance that can overwrite remote branch history. <br>
Mitigation: Use any force-push workflow only on branches you control and only after confirming the remote state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shinelp100/skill-publish-tool) <br>
- [Usage guide](USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute local file edits, Git operations, and ClawHub publishing steps depending on user intent.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
