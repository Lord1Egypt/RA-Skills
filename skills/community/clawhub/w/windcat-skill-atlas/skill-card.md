## Description: <br>
Skill Atlas helps an agent manage OpenClaw skills by guiding installation, updates, rollback, backups, security review, and loading-layer decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guowenjiao54](https://clawhub.ai/user/guowenjiao54) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Skill Atlas to manage local skills, manifests, backups, channels, and layer assignments in an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide changes to installed skills, manifests, backups, and loading layers, including uninstall, rollback, bulk restore, bulk update, or promotion to resident or core behavior. <br>
Mitigation: Require explicit confirmation for those operations and review which files will change before allowing them. <br>
Risk: Incorrect channel, manifest, or layer changes could alter future skill loading behavior. <br>
Mitigation: Confirm the target skill, channel, version, and layer before applying manifest or loading-rule changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guowenjiao54/windcat-skill-atlas) <br>
- [reference.md](reference.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with command and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file changes for skill manifests, backups, and installed skill directories.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
