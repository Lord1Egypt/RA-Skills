## Description: <br>
Creates Word-compatible .docx documents from structured HTML and edits existing DOCX files through text replacement, unpacking, repacking, and validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixihaha123123123123](https://clawhub.ai/user/xixihaha123123123123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-producing agents use this skill to generate WPS/Word-compatible .docx deliverables from HTML or to make controlled text replacements in existing Word documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTML-to-DOCX conversion can contact remote image URLs embedded in input HTML. <br>
Mitigation: Use trusted HTML, prefer local or embedded images, and avoid converting untrusted HTML that references remote image URLs. <br>
Risk: DOCX unpacking can remove the selected output directory before extraction. <br>
Mitigation: Run the skill in a dedicated working directory and never point unpack output at a folder containing important files. <br>
Risk: The server security verdict is suspicious even though static scanning was clean. <br>
Mitigation: Review the skill before installing and inspect generated or modified documents before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xixihaha123123123123/wps-docx) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Guidance] <br>
**Output Format:** [DOCX files with supporting HTML or Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated DOCX output should be validated and reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
