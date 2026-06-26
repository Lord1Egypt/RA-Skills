## Description: <br>
Combine multiple image screenshots into a paginated A4 PDF, with page-break handling that aims to avoid cutting through text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxttt](https://clawhub.ai/user/wxttt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to combine image files or image directories into a print-ready A4 PDF, especially for screenshots, exam papers, and document photos. The agent identifies the input and output paths, runs the bundled Python script, and reports the processed image count, generated page count, and output path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill may download Pillow and numpy through uv. <br>
Mitigation: Review dependency installation in the execution environment before running the command. <br>
Risk: The script writes a PDF to the chosen path, or to output.pdf by default. <br>
Mitigation: Use an explicit output filename and check whether the target file already exists before execution. <br>
Risk: The skill processes local images supplied by the user. <br>
Mitigation: Run it only on intended local image files and avoid including sensitive images unless the local execution environment is appropriate. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wxttt/smart-image-to-pdf) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Image-to-PDF script](artifact/scripts/combine.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and a generated PDF file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local PDF at the requested output path, or output.pdf by default.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
