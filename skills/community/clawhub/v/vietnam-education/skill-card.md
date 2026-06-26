## Description: <br>
Vietnam Education helps agents draft Vietnamese lesson plans, exam papers, worksheets, answer checks, and supporting figures aligned with CTGDPT 2018 and CV 7991/BGDDT-GDTrH. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trustydev212](https://clawhub.ai/user/trustydev212) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers, education content creators, and agents supporting Vietnamese curricula use this skill to prepare lesson plans, structured tests, worksheets, answer verification steps, and document-generation commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local helper scripts parse free-form formulas and expressions without a clearly bounded safety model. <br>
Mitigation: Run the scripts in a virtual environment or isolated project directory, install dependencies locally, and only pass expressions that have been reviewed or come from trusted lesson content. <br>
Risk: Generated educational content and answer keys can be wrong or outdated if source material is not checked. <br>
Mitigation: Verify curriculum facts against current source materials and review all generated questions, answers, figures, and documents before classroom use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/trustydev212/vietnam-education) <br>
- [OpenClaw Viet Nam community](https://zalo.me/g/lajsqc334jqc5fezevvo) <br>
- [CTGDPT 2018 reference](references/ctgdpt-2018.md) <br>
- [CV 7991, lesson plan, and worksheet templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, editable script configuration, and generated .docx or image files when helper scripts are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and node; helper scripts rely on local project dependencies such as docx, SymPy, Matplotlib, and NumPy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
