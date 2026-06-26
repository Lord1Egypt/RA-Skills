## Description: <br>
Creates structured vendor-risk briefs for external SaaS/API integrations, focusing on integration impact, requested permissions, data flows, mitigations, alternatives, and recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, procurement reviewers, security teams, and developers use this skill to turn scoped vendor capability, permission, and data-type inputs into a reviewable vendor-risk brief before procurement or integration decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated briefs may be mistaken for formal legal or security approval. <br>
Mitigation: Use the output as a draft vendor-risk summary and route final approval through the organization's normal legal and security review process. <br>
Risk: Inputs may include secrets, personal data, or sensitive vendor details. <br>
Mitigation: Provide scoped inputs, remove unnecessary sensitive data before use, and review generated output before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/vendor-risk-brief) <br>
- [README.md](README.md) <br>
- [resources/spec.json](resources/spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Structured Markdown or JSON report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-selected input file, directory, or inline text; can print to stdout or write a user-selected output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
