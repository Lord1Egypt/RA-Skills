## Description: <br>
Use when bulk-managing Terraform modules at scale: upgrading providers across AWS, GCP, Azure, or DigitalOcean repositories, standardizing GitHub Actions workflows, automating semantic releases, running security scans, or performing end-to-end maintenance cycles across 10-200+ module repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, DevOps engineers, and platform teams use this skill to coordinate Terraform module maintenance across many repositories, including provider upgrades, workflow standardization, validation, changelog generation, and release creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically change many repositories and publish GitHub releases. <br>
Mitigation: Run it first against a small test repository, require explicit repository lists, inspect diffs before committing, and avoid direct pushes or release creation until reviewed. <br>
Risk: Automation may use GitHub credentials with write permissions. <br>
Mitigation: Use narrowly scoped GitHub tokens, prefer repository-specific access, and enable review gates such as pull requests before merging. <br>
Risk: Configuration files are loaded by shell scripts and can affect executed commands. <br>
Mitigation: Treat configuration files as executable shell code, review them before use, and keep secrets out of configuration files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anmolnagpal/terraform-ai-skills) <br>
- [Project homepage](https://github.com/anmolnagpal/terraform-ai-skills) <br>
- [Provider Configs](references/provider-configs.md) <br>
- [Safety & Rollback](references/safety.md) <br>
- [Real-World Examples](references/examples.md) <br>
- [Quick Reference](references/quick-reference.md) <br>
- [Security Policy](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, configuration references, and generated repository maintenance steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to run Terraform, Git, GitHub CLI, and validation tools against selected repositories.] <br>

## Skill Version(s): <br>
0.0.2 (source: SKILL.md frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
