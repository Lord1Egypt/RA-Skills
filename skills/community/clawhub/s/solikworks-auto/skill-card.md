## Description: <br>
Generates Python pywin32 code that controls SolidWorks through its official COM interface to automate part creation, sketching, feature generation, drawing export, and file saving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2009730](https://clawhub.ai/user/2009730) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Mechanical designers, engineers, and agents use this skill to turn SolidWorks modeling or drawing requests into runnable Python scripts and execution guidance for local SolidWorks automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Python scripts can control SolidWorks and write files. <br>
Mitigation: Review dimensions, filenames, output paths, overwrite behavior, and the generated code before running it locally. <br>
Risk: The workflow depends on pywin32 and local COM automation access. <br>
Mitigation: Install pywin32 only from trusted sources and run the script in an environment where SolidWorks automation is expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2009730/solikworks-auto) <br>
- [Publisher profile](https://clawhub.ai/user/2009730) <br>


## Skill Output: <br>
**Output Type(s):** [code, markdown, guidance] <br>
**Output Format:** [Markdown with Python code blocks and step-by-step run and verification guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated scripts are intended for local Windows SolidWorks environments with Python, pywin32, and COM access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
