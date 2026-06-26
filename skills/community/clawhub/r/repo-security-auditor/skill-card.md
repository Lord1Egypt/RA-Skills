## Description: <br>
Audits GitHub repositories for security vulnerabilities, suspicious behavior, dependency risks, license compatibility, and clean reimplementation planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erickgrau](https://clawhub.ai/user/erickgrau) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to assess third-party repositories before adopting, forking, or reimplementing them. It helps identify suspicious code patterns, dependency vulnerabilities, license concerns, and whether a clean reimplementation is appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads repositories that may contain untrusted code and stores audit reports locally. <br>
Mitigation: Run audits in a disposable or project-specific workspace, avoid executing cloned code unless separately trusted, and periodically clean up retained audit artifacts. <br>
Risk: Security findings from automated scans can miss context or produce false positives. <br>
Mitigation: Treat generated reports as review inputs and manually verify important findings before adopting or reimplementing a repository. <br>


## Reference(s): <br>
- [Repo Security Auditor on ClawHub](https://clawhub.ai/erickgrau/repo-security-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON risk assessments, shell commands, and optional project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local audit artifacts and optional clean-scaffold files when a repository is judged safe.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
