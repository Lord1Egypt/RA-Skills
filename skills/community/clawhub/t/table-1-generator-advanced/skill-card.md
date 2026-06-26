## Description: <br>
Automated generation of baseline characteristics tables (Table 1) for clinical research papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical researchers, analysts, and developers use this skill to generate reproducible baseline characteristics tables from patient CSV data, including variable type detection, group comparisons, missing data reporting, and publication-oriented formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical input CSVs and generated tables may contain sensitive patient information. <br>
Mitigation: Run the skill only on intended datasets in a controlled workspace and review outputs for identifiers or small-cell disclosure before sharing. <br>
Risk: Unpinned numpy, pandas, and scipy versions can affect repeatability in regulated or audited research. <br>
Mitigation: Install in a virtual environment and pin or lock dependency versions before regulated or repeatable use. <br>
Risk: Local file reads and output writes can target unintended paths if command arguments are not controlled. <br>
Mitigation: Validate the input and output paths before execution and keep generated files inside an approved workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/table-1-generator-advanced) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated CSV table artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-provided CSV files locally and can write Table 1 output to a requested CSV path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
