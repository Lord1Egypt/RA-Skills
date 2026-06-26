## Description: <br>
Security checks for installing skills, packages, or plugins before install commands or first use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sudhindrat](https://clawhub.ai/user/sudhindrat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to pause skill, package, or plugin installs for a brief security review before proceeding. It provides a practical checklist for source reputation, dependency risk, lifecycle scripts, dynamic content, credential exposure, and post-install review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install reviews can miss malicious behavior if users treat checklist guidance as automatic approval. <br>
Mitigation: Use the skill as a pause-and-review checklist, and separately approve any install, audit-fix, or other mutating command. <br>
Risk: Packages, skills, or plugins may run lifecycle scripts, fetch dynamic content, or access credentials after installation. <br>
Mitigation: Review source, dependency metadata, lifecycle scripts, external network access, file writes, and credential-path references before first use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown checklist with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
