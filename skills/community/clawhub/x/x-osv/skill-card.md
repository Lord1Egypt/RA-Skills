## Description: <br>
x-osv helps agents guide users through querying the Google OSV vulnerability database, scanning local projects with osv-scanner, and generating SARIF vulnerability reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwinjhlee](https://clawhub.ai/user/edwinjhlee) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and security engineers use this skill to query open source vulnerability data for packages, inspect vulnerability records, and run dependency scans against intended project directories or lockfiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on external x-cmd and osv-scanner tooling that users install separately. <br>
Mitigation: Install those tools only from trusted sources before following generated commands. <br>
Risk: Project scans can inspect local directories or lockfiles beyond the user's intended target. <br>
Mitigation: Run scans only against project directories or lockfiles the user explicitly intends to analyze. <br>


## Reference(s): <br>
- [OSV.dev](https://osv.dev) <br>
- [osv-scanner](https://github.com/google/osv-scanner) <br>
- [x-osv on ClawHub](https://clawhub.ai/edwinjhlee/x-osv) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown with inline bash command examples and command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include prerequisite guidance for installing x-cmd and osv-scanner.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
