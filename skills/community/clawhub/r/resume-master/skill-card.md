## Description: <br>
Resume Master helps users create new resumes or tailor existing resumes to job descriptions by writing editable HTML source files and exporting print-ready PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyafu](https://clawhub.ai/user/wangyafu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to build, revise, and job-target resumes for job searches, study applications, and similar career workflows. The skill guides resume content collection, HTML authoring, PDF export, page-count checks, and visual review from rendered PDF pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled HTML templates may request remote fonts or images during rendering. <br>
Mitigation: Remove or replace remote template links and images before rendering when privacy or network disclosure is a concern. <br>
Risk: Resume workflows may process sensitive personal details in generated HTML, PDF, Markdown, and image files. <br>
Mitigation: Keep generated files local, review their contents before sharing, and render only HTML that the user trusts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyafu/resume-master) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [JD example](artifact/assets/examples/jd.example.txt) <br>
- [HTML template references](artifact/assets/template_refs/html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with HTML source files, PDF files, and optional PNG/JPG review images] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local .html, .pdf, .changes.md, and per-page image files during resume workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
