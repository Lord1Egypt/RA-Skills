## Description: <br>
Shows a folder's files and subdirectories as an indented directory tree. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinwangmok](https://clawhub.ai/user/jinwangmok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users use this skill to inspect a local folder's visible file and subdirectory structure before navigating or discussing project contents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Directory listings can reveal file and folder names that the user may not want shared in chat. <br>
Mitigation: Run the skill only on folders whose visible names are acceptable to disclose. <br>
Risk: Large directory trees can produce noisy or excessive output. <br>
Mitigation: Use a small depth value for large directories. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text directory tree with optional Markdown code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local find, sort, and sed; accepts optional directory and depth arguments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
