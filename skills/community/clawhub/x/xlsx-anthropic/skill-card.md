## Description: <br>
Helps agents create, edit, analyze, clean, format, and verify spreadsheet files such as .xlsx, .xlsm, .csv, and .tsv deliverables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pupuking723](https://clawhub.ai/user/pupuking723) <br>

### License/Terms of Use: <br>
Anthropic proprietary terms <br>


## Use Case: <br>
Developers and agent users use this skill when a spreadsheet is the primary input or output, including workbook creation, existing-file edits, tabular cleanup, formula construction, formatting, and post-edit formula verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-impact LibreOffice process changes may affect document handling outside ordinary spreadsheet editing expectations. <br>
Mitigation: Install and run the skill only in an isolated workspace until the LibreOffice behavior is narrowed, clearly gated, and documented. <br>
Risk: The artifact includes DOCX and PPTX tooling outside the stated spreadsheet-focused scope. <br>
Mitigation: Avoid sensitive Office documents and review or disable non-spreadsheet tooling before deployment. <br>
Risk: Persistent LibreOffice profile macros and a fixed-temp LD_PRELOAD shim are called out in the security guidance. <br>
Mitigation: Require publisher changes that remove persistent macros and replace the shim with a safer documented mechanism before broad use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pupuking723/xlsx-anthropic) <br>
- [Artifact license terms](artifact/LICENSE.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets; spreadsheet files may be produced by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill emphasizes dynamic spreadsheet formulas, LibreOffice recalculation, and formula-error checks before delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
