## Description: <br>
Guides agents through Python packaging workflows for pyproject metadata, dependency separation, build backends, wheels, versioning, publishing, and CI release hygiene for libraries and CLI tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codekungfu](https://clawhub.ai/user/codekungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and review Python package releases for libraries and CLI tools, including project layout, metadata, dependencies, build artifacts, versioning, and secure CI publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A release could target the wrong package index, version, or build artifacts. <br>
Mitigation: Confirm the target index, package version, wheel, and sdist before running a real release. <br>
Risk: Broad or long-lived publishing credentials can expose package indexes if leaked. <br>
Mitigation: Prefer OIDC trusted publishing or use tightly scoped, short-lived credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codekungfu/python-packaging) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown guidance with checklists and inline command or configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include packaging checklists, release steps, and CI publishing safety recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
