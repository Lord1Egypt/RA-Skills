## Description: <br>
Splits large text files into smaller chunks by line count for easier processing of logs, datasets, or documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use TXT Chunker to split large logs, datasets, or long documents into smaller text files by line count for easier processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chunk output files are written in the current directory or the path implied by the output prefix, and matching filenames may be overwritten. <br>
Mitigation: Run the tool in a dedicated output directory or choose a unique output prefix before processing important files. <br>
Risk: The documented command name may not be installed as a wrapper in every environment. <br>
Mitigation: If the wrapper is unavailable, run the bundled Python script directly with the same input file, line-count, and output-prefix arguments. <br>


## Reference(s): <br>
- [Txt Chunker ClawHub listing](https://clawhub.ai/albionaiinc-del/txt-chunker) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with CLI examples and generated text chunk files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes chunk files using the selected output prefix and numbered .txt filenames.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
