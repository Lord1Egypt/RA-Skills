## Description: <br>
Converts Tsinghua University thesis Word documents into thuthesis-compatible LaTeX projects and PDFs, including chapter structure, abstracts, figures, tables, references, acknowledgements, resumes, lists, and evaluation reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chao1208](https://clawhub.ai/user/chao1208) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert Tsinghua thesis .docx files into a compilable thuthesis LaTeX/PDF project and to review formatting quality before submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled output files contain identifiable personal and academic thesis data that is not required for the converter to run. <br>
Mitigation: Review or remove bundled output/ files before installing, sharing, or storing the skill locally. <br>
Risk: Generated citations, tables, figures, and LaTeX changes may be incorrect or incomplete for academic submission. <br>
Mitigation: Review generated references and LaTeX changes against the source Word document before submission. <br>
Risk: Setup and LaTeX compilation operate on local files and external template sources. <br>
Mitigation: Run setup and compilation in a controlled workspace, using filesystem isolation where possible. <br>


## Reference(s): <br>
- [thuthesis official template](https://github.com/tuna/thuthesis) <br>
- [thu-thesis ClawHub release page](https://clawhub.ai/chao1208/thu-thesis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands plus JSON, LaTeX project files, BibTeX, PDFs, and evaluation reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local thesis conversion workspaces; generated citations, tables, figures, and LaTeX should be reviewed before academic submission.] <br>

## Skill Version(s): <br>
1.5.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
