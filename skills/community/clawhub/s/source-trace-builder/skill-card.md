## Description: <br>
Builds a citation index and original-source mapping for analysis drafts, while distinguishing primary and secondary sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, auditors, and developers use this skill to organize draft source material into reviewable source directories, primary/secondary-source distinctions, citation mappings, missing-source notes, risk notes, and maintenance suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local helper reads the input file selected by the user, which may contain sensitive drafts or source notes. <br>
Mitigation: Use dry-run or stdout for sensitive drafts, redact private material before processing, and choose input files deliberately. <br>
Risk: Generated citation mappings and source distinctions may be incomplete when the input lacks enough source clues. <br>
Mitigation: Review the missing-source and risk-note sections before relying on the report. <br>
Risk: Supplying an output path causes the helper to write a report file locally. <br>
Mitigation: Choose output paths deliberately and prefer stdout when a file artifact is not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/source-trace-builder) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [Skill README](artifact/README.md) <br>
- [Structured output spec](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown by default, with optional JSON from the local helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a report file when an output path is supplied, or print to stdout/dry-run for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
