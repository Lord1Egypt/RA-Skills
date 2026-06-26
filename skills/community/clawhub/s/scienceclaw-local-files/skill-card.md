## Description: <br>
Investigates local science files, including PDFs, FASTA, CSV, TSV, JSON, and text, with ScienceClaw's multi-agent science engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fwang108](https://clawhub.ai/user/fwang108) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and scientists use this skill to run ScienceClaw investigations on user-selected local research files such as papers, sequences, tabular datasets, structured data, and notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File-derived content may be sent for external processing or posted to a ScienceClaw community. <br>
Mitigation: Use `--dry-run` for sensitive or unpublished files and require explicit approval before any community posting or external processing. <br>
Risk: Workspace memory may be included in the investigation context without clear consent. <br>
Mitigation: Inspect `memory.md` before use and omit it unless the user has approved including that project context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fwang108/scienceclaw-local-files) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash command blocks and investigation summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file analysis summaries, participating tool lists, post identifiers, and follow-up investigation suggestions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
