## Description: <br>
Resume Editor helps agents build, edit, validate, and export professional resumes with PDF import, styled HTML/PDF output, language labels, and theme customization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chijiang](https://clawhub.ai/user/chijiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill through an AI agent to create, revise, validate, and export resumes or CVs while keeping resume data local. It is suited for workflows that need structured resume JSON, styled HTML/PDF output, editable review, multilingual labels, or reusable themes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume files can contain sensitive personal data. <br>
Mitigation: Install and use only when comfortable with a local resume tool that reads and writes those files, and keep editable HTML outputs private. <br>
Risk: Editable HTML can start a local write-back sync server that may continue running after editing. <br>
Mitigation: Use editable mode only when needed, stop the sync server when finished, and avoid sharing editable HTML artifacts. <br>
Risk: Theme scaffolding can overwrite or remove files when forced or pointed at arbitrary output directories. <br>
Mitigation: Avoid `--force` and arbitrary `--output-dir` values unless backups exist and the target directory has been checked. <br>
Risk: PDF import depends on a PDF parsing package and may process untrusted files. <br>
Mitigation: Update or isolate the PDF dependency before opening untrusted PDFs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chijiang/skills/resume-editor) <br>
- [README](README.md) <br>
- [Resume Schema](references/resume-schema.json) <br>
- [Resume Data Structure](references/data-structure.md) <br>
- [Customization](references/customization.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, structured JSON resume files, and generated HTML or PDF resume files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local editable HTML and final non-editable HTML/PDF outputs; PDF import and export require optional pinned Python dependencies.] <br>

## Skill Version(s): <br>
1.3.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
