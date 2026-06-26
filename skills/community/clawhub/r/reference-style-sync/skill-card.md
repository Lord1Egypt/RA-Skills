## Description: <br>
One-click synchronization and standardization of reference formats in literature management tools, intelligently fixing metadata errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, academic writers, and developers use this skill to clean, normalize, convert, deduplicate, and quality-check citation libraries exported from Zotero, EndNote, or universal formats such as BibTeX, RIS, CSV, and JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Citation libraries may contain customer, research, or unpublished metadata that should not be shared or written outside an authorized workspace. <br>
Mitigation: Use only inputs the operator is authorized to process and review output paths before running the packaged script. <br>
Risk: Automated metadata repair can produce incorrect citations because DOI checks are pattern-based and journal or author normalization uses built-in rules. <br>
Mitigation: Review changed records, especially DOI, journal abbreviation, author, and page fields, before using the resulting bibliography in publication or compliance workflows. <br>
Risk: The artifact includes a local Python script that reads input files and writes output files. <br>
Mitigation: Run it in a sandboxed workspace, inspect command arguments, and back up the source library before batch processing. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/reference-style-sync) <br>
- [AIpoch publisher profile](https://clawhub.ai/user/aipoch-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated bibliography or citation-library files when the packaged script is run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Works with local citation-library inputs and may write normalized output files to the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
