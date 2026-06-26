## Description: <br>
Merges local image files into multipage TIFF files and offers a TIFF page-splitting workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fly3094](https://clawhub.ai/user/fly3094) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to process local image files into TIFF outputs without uploading files. The split workflow should be treated cautiously because release security guidance says it is incomplete until fixed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The TIFF split feature may report PNG or JPG output paths without actually writing those image files. <br>
Mitigation: Confirm expected output files exist after split operations and treat the split feature as incomplete until the author fixes it. <br>
Risk: The skill reads and writes local image files at user-supplied paths. <br>
Mitigation: Confirm input and output paths before execution and run it only on files intended for local TIFF processing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fly3094/tiff-merge) <br>
- [UTIF.js](https://github.com/photopea/UTIF.js) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local TIFF file paths for merge workflows; split output paths may be reported before actual PNG or JPG files are written.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
