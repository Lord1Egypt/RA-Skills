## Description: <br>
Batch process chemical SMILES strings to remove salt ion components and retain the active core compound. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cheminformatics analysts, and data teams use this skill to clean batches of chemical SMILES strings by removing counterions or salt fragments before review or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged script writes to the user-specified output path and can overwrite an existing file. <br>
Mitigation: Choose an explicit workspace output path, check whether the target file already exists, and keep a backup when replacing prior results. <br>
Risk: Dependency versions for pandas and RDKit affect reproducibility of parsing and output behavior. <br>
Mitigation: Install in a virtual environment and pin or review pandas and RDKit versions before running production or regulated workflows. <br>
Risk: The de-salting logic uses heuristics such as retaining the largest component, which may be wrong for co-crystals or multi-component compounds. <br>
Mitigation: Sample and manually review representative outputs, especially for co-crystals, quaternary ammonium salts, and multi-component drug records. <br>


## Reference(s): <br>
- [SMILES De-salter release page](https://clawhub.ai/aipoch-ai/smiles-de-salter) <br>
- [AIpoch publisher profile](https://clawhub.ai/user/aipoch-ai) <br>
- [Runtime Checklist](references/runtime_checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and CSV, TSV, or text file outputs from the packaged script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script adds desalted_smiles and status columns for file processing, or prints the desalted SMILES and status for a single input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and script header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
