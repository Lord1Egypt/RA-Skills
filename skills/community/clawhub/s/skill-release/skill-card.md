## Description: <br>
Publish and manage Claude Code skills on ClawHub, including first-time publishing, version updates, readiness checks, and changelog support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperkwok](https://clawhub.ai/user/casperkwok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this agent skill to check ClawHub CLI readiness, validate skill metadata, publish new Claude Code skills, update existing releases, and prepare version or changelog information before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a ClawHub token or logged-in account to publish or update releases. <br>
Mitigation: Use a token or account with only the permissions needed for publishing, and verify the ClawHub account before publishing. <br>
Risk: The skill may edit SKILL.md version metadata and publish the selected target directory. <br>
Mitigation: Run the check or dry-run flow first, then verify the target directory, slug, version, and changelog before allowing publication. <br>


## Reference(s): <br>
- [Skill Release on ClawHub](https://clawhub.ai/casperkwok/skill-release) <br>
- [Publisher profile: casperkwok](https://clawhub.ai/user/casperkwok) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and possible skill file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run ClawHub CLI checks, suggest version bumps and changelog text, and update SKILL.md when publishing an updated release.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
