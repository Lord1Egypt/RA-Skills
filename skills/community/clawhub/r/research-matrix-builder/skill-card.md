## Description: <br>
Build literature matrices from papers, notes, and abstracts to compare methods, data, findings, and research gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and review authors use this skill to turn paper lists, notes, abstracts, and research questions into literature comparison matrices, thematic clusters, gap summaries, and review outlines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags a review helper that may run a nested agent with broad local authority. <br>
Mitigation: Install only from a trusted publisher, prefer no-yolo review modes, and grant full local authority only when it is explicitly required. <br>
Risk: Generated literature matrices can contain unsupported or incomplete claims if source notes are sparse. <br>
Mitigation: Keep missing fields explicit, cite source material where possible, and review the matrix before using it in formal research outputs. <br>
Risk: The bundled helper can write a CSV file to the requested output path. <br>
Mitigation: Use explicit input and output paths and preview generated content before overwriting or distributing files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/research-matrix-builder) <br>
- [Publisher Profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [README.md](README.md) <br>
- [Matrix Schema](resources/matrix_schema.csv) <br>
- [Build Matrix Script](scripts/build_matrix.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CSV-compatible matrix output and optional local file generation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a bundled python3 helper to convert JSON paper records into a CSV literature matrix.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
