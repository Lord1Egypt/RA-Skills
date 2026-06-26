## Description: <br>
Generate a polished PDF report or summary from findings, data, or tables gathered earlier in the conversation, producing Typst source, compiling it with Typst, and reporting the output path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seitzbg](https://clawhub.ai/user/seitzbg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn previously gathered findings, tables, and summaries into clean local PDF reports. It is useful when a conversation needs a polished deliverable rather than only chat text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes generated PDF and Typst source files to the working directory or selected output path, which can leave report contents on disk. <br>
Mitigation: Choose an output path appropriate for the report contents and avoid shared or sensitive folders unless local storage is acceptable. <br>
Risk: The skill runs the Typst compiler to produce the PDF. <br>
Mitigation: Install and use a trusted Typst binary, then review compile errors and generated files before sharing the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seitzbg/skeet-pdf-report) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with Typst source guidance and shell commands; generated local .typ and .pdf files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Typst binary and writes both the PDF and the Typst source file in the working directory or chosen output path.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
