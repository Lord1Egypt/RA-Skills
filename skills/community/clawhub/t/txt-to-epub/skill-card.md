## Description: <br>
Converts TXT text into EPUB files using rule-based chapter recognition and splitting for novels, tutorials, and other long-form text, with no built-in AI interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1oid](https://clawhub.ai/user/1oid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to convert local TXT manuscripts, tutorials, and long-form documents into EPUB files with navigable chapter structure. It helps choose split settings, run the bundled converter, and report the output path, chapter count, and title preview. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter creates an EPUB next to the input TXT by default, which can be unexpected or overwrite a same-named output file. <br>
Mitigation: Use an explicit --output path and review the destination before running the conversion. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with shell commands and conversion results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for running a local Python converter that writes an EPUB file and prints the output path, detected encoding, split method, chapter count, and chapter preview.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
