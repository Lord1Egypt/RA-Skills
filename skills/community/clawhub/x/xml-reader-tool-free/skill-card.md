## Description: <br>
XML读取器免费版 helps agents read and browse XML files, traverse nodes, run basic XPath queries, format output, and summarize XML structure for developer review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to inspect XML configuration or data files, locate nodes with XPath, format XML for readability, and generate basic structure statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports inconsistent documentation about whether the skill may write, modify, delete, import, export, or save files. <br>
Mitigation: Treat the skill as review-worthy before installation, grant only the minimum file permissions needed for XML reading, and avoid write, export, modify, delete, import, or save workflows until the publisher clarifies the free edition behavior. <br>
Risk: The artifact states that the free edition loads XML files into memory and recommends files no larger than 50 MB. <br>
Mitigation: Use the skill on small or known-size XML files, inspect file size before running broad queries, and use a streaming XML workflow for larger files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/xml-reader-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and text or XML output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free edition documentation describes terminal-oriented output and read/query workflows, but security evidence flags inconsistent write and export behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
