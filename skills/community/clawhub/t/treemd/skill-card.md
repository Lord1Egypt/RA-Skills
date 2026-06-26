## Description: <br>
Markdown document analysis and navigation using the treemd CLI for heading trees, section extraction, tql queries, and programmatic Markdown inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wei840222](https://clawhub.ai/user/wei840222) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect, navigate, query, and extract content from Markdown documents without loading entire large files into context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external treemd CLI binary. <br>
Mitigation: Install treemd only from a trusted source and verify the binary before use. <br>
Risk: Markdown files inspected by the agent may contain sensitive content. <br>
Mitigation: Use the skill only on Markdown files that are appropriate for the agent to inspect. <br>


## Reference(s): <br>
- [treemd Query Language Reference](references/query-language.md) <br>
- [treemd project](https://github.com/Epistates/treemd) <br>
- [treemd releases](https://github.com/Epistates/treemd/releases) <br>
- [ClawHub skill page](https://clawhub.ai/wei840222/treemd) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, JSON, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and treemd output format notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external treemd CLI binary.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
