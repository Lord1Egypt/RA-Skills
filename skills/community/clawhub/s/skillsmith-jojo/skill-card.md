## Description: <br>
Skillsmith-JOJO is a local toolkit that helps developers create, test, security-check, analyze, package, and publish OpenClaw skills from reusable templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skillforge-jojo](https://clawhub.ai/user/skillforge-jojo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to scaffold OpenClaw skills, apply development best practices, run local quality and security checks, analyze token footprint, and prepare releases for ClawHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Git helper and publishing workflows can change repository state or release content. <br>
Mitigation: Review the target repository and require explicit confirmation before commit, branch, file move, file delete, rename, or publish workflows. <br>
Risk: API-oriented templates and local checks may involve credentials or scans over an unintended target path. <br>
Mitigation: Use environment variables for tokens, avoid hardcoded secrets, and verify the target directory before running tests or security scans. <br>


## Reference(s): <br>
- [Skill Design Best Practices](references/best-practices.md) <br>
- [ClawHub Publishing Guide](references/publishing.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/skillforge-jojo/skillsmith-jojo) <br>
- [Publisher Profile](https://clawhub.ai/user/skillforge-jojo) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python scripts, and template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workflow guidance, reusable skill templates, test reports, security scan output, token analysis, and Git helper command results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
