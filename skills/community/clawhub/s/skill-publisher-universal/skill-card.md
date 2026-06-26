## Description: <br>
Generic publishing tool for Claude Code skills that validates, packages, and publishes to ClawHub, Hermes Agent, and anthropics/skills with bilingual README support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyanbo2007](https://clawhub.ai/user/zhangyanbo2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to validate Claude Code skill metadata, generate publish packages and bilingual README files, and prepare publishing steps for ClawHub, Hermes Agent, and anthropics/skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may direct an agent to read local GitHub and ClawHub credentials from ~/.env or the shell environment. <br>
Mitigation: Require explicit user confirmation before reading credential files or environment variables, and use least-privilege tokens scoped only to the intended publish target. <br>
Risk: Publishing, branch pushes, pull requests, and proxy changes can affect external accounts or local network behavior. <br>
Mitigation: Confirm the target platform, repository, branch, and proxy settings before making changes, and prefer dry-run validation before any upload or push. <br>
Risk: Generated publish packages may contain copied scripts, manifests, README content, or examples that were not intended for release. <br>
Mitigation: Inspect the generated package contents and run validation or scanning before uploading to ClawHub or submitting GitHub pull requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhangyanbo2007/skill-publisher-universal) <br>
- [Publisher Profile](https://clawhub.ai/user/zhangyanbo2007) <br>
- [Hermes Agent GitHub API Endpoint](https://api.github.com/repos/NousResearch/hermes-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated files, manifests, and validation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local publish package artifacts such as SKILL.md, README.md, scripts, examples, and .clawhub.json when helper scripts are run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
