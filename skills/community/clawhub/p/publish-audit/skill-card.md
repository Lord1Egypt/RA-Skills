## Description: <br>
Audits ClawHub skill folders before publishing by checking frontmatter, runtime metadata, secret handling, file limits, and publish-readiness issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solidstate](https://clawhub.ai/user/solidstate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to audit a ClawHub skill folder before publishing. It produces a concise readiness report with blockers, warnings, and concrete fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit guidance may discuss sensitive local skill contents, including possible secret references. <br>
Mitigation: Run it only on skill folders intended for review and inspect the generated report before applying suggested fixes. <br>
Risk: The skill is a publish-readiness audit, not a full install-safety or malware vetter. <br>
Mitigation: Use a separate vetting process before installing third-party skills. <br>


## Reference(s): <br>
- [Publish Audit skill page](https://clawhub.ai/solidstate/publish-audit) <br>
- [Solid State homepage](https://solidstate.cc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown audit report with pass, warning, blocker, verdict, and publish command sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local skill folders and returns review guidance; it does not make network calls or use credentials.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
