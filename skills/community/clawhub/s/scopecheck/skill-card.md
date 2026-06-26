## Description: <br>
Analyze an OpenClaw SKILL.md and extract its permission scope, including environment variables, CLI tools, filesystem paths, and network URLs, while comparing declared requirements against detected access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill reviewers use Scopecheck to analyze a SKILL.md file's declared requirements and compare them with detected environment variables, CLI tools, filesystem paths, and network URLs before release or installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scope detection is heuristic and may flag examples or documentation text as access, or miss behavior that is not visible in SKILL.md text. <br>
Mitigation: Treat results as a review aid and inspect the source skill before relying on findings for release or installation decisions. <br>
Risk: Submitted SKILL.md content can contain sensitive private instructions or secrets. <br>
Mitigation: Run the analyzer locally and avoid submitting highly sensitive skill text unless it is needed for review. <br>


## Reference(s): <br>
- [Scopecheck on ClawHub](https://clawhub.ai/mirni/scopecheck) <br>


## Skill Output: <br>
**Output Type(s):** [json, guidance, shell commands] <br>
**Output Format:** [JSON scope analysis with setup and curl usage commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports declared requirements, detected access, and undeclared access prefixes for environment variables, binaries, filesystem paths, and network URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
