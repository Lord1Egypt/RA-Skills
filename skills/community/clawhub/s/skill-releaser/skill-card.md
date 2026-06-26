## Description: <br>
Release skills to ClawhHub through the full publication pipeline: auto-scaffolding, OPSEC scan, dual review, force-push release, security scan verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunhualiao](https://clawhub.ai/user/chunhualiao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and release maintainers use this skill to prepare, review, stage, publish, and verify ClawhHub skill releases from a completed SKILL.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release workflow can make repository and registry changes public, including force-push and visibility changes. <br>
Mitigation: Review the exact staging directory and target repository before approval, use least-privilege GitHub and ClawhHub accounts, and require explicit approval before public release actions. <br>
Risk: The authoritative security summary flags a flawed security gate and unpinned local tooling before publication. <br>
Mitigation: Do not rely on the OPSEC gate alone until the fail-open bug and local helper provenance are fixed; independently verify credentials, target paths, and release contents before publishing. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/chunhualiao/skill-releaser) <br>
- [README](artifact/README.md) <br>
- [Release Validation Scripts](artifact/scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command blocks and generated release files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates privileged git, gh, browser, filesystem, and clawhub CLI actions with explicit approval gates for public release steps.] <br>

## Skill Version(s): <br>
1.5.0 (source: release evidence, SKILL.md frontmatter, skill.yml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
