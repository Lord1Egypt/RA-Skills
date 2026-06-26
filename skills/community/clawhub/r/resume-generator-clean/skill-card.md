## Description: <br>
Generates professional resumes and CVs with PDF, Word, and HTML export from YAML, Markdown, HTML, or Python inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[31504254](https://clawhub.ai/user/31504254) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, job seekers, and academic users use this skill to create or convert resumes and CVs into print-ready PDF, editable Word, or HTML outputs. It is suited for local document generation workflows that need templates, auto-layout, and Chinese/English text support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unaudited Python dependencies or optional document-conversion backends can create supply-chain or compatibility risk. <br>
Mitigation: Install in a virtual environment and pin or audit dependencies before use. <br>
Risk: Converting untrusted HTML or Markdown may allow PDF or HTML renderers to process local resources. <br>
Mitigation: Use trusted input files and review conversion behavior before processing external documents. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/31504254/resume-generator-clean) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Example resume YAML](examples/example_resume.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with bash and Python examples; generated artifacts may be PDF, DOCX, or HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts YAML, Markdown, HTML, and Python API inputs; optional PDF backends can affect output fidelity.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
