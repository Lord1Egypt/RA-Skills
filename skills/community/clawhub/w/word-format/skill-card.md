## Description: <br>
Converts user-provided Word documents into a fixed Chinese official-document format using the bundled template settings and deterministic paragraph heuristics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nighmat1220](https://clawhub.ai/user/Nighmat1220) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, document operations teams, and agents use this skill to restyle uploaded .docx files into a standard government-style Word format. It is suited for repeatable formatting of titles, body text, headings, tables, attachments, dates, signatures, margins, and font choices before human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter runs locally on user-provided Word files and writes a new output file. <br>
Mitigation: Keep original documents backed up and choose the output path deliberately before running the conversion. <br>
Risk: Required fonts may be unavailable, preventing faithful formatting. <br>
Mitigation: Check the missing-font notice, install the listed fonts, and rerun the converter instead of using a partial result. <br>
Risk: Complex layouts may not be fully captured by deterministic paragraph and table heuristics. <br>
Mitigation: Manually review converted documents, especially files with unusual sectioning, tables, attachments, or mixed formatting. <br>


## Reference(s): <br>
- [Format Rules](references/format-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [DOCX file with concise Markdown status or missing-font notice] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Python execution against a user-provided .docx file and installed Chinese fonts; complex layouts should be manually reviewed after conversion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
