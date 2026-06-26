## Description: <br>
Enhanced `uname` command with colorized, structured output that shows hostname, OS, kernel, architecture, and version. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwinjhlee](https://clawhub.ai/user/edwinjhlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill for guidance on running `x uname` to inspect basic system information in a structured, readable format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The separate x-cmd dependency is required but was not included in the security review. <br>
Mitigation: Install x-cmd only from a trusted source and review that dependency before relying on this skill. <br>
Risk: `x uname` output may reveal host and kernel details if shared from sensitive systems. <br>
Mitigation: Avoid publishing command output from sensitive environments unless hostname, kernel, and OS version details are acceptable to disclose. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edwinjhlee/x-uname) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents command output fields for hostname, OS name, kernel, machine architecture, and OS version.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
