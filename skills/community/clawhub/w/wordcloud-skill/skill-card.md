## Description: <br>
Generates a word cloud image from provided text, a Markdown file, or a directory of Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijiahao885](https://clawhub.ai/user/lijiahao885) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content authors use this skill to create PNG word cloud visualizations from text or Markdown sources, with optional dimensions, mask image, font, stop words, and output directory controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local text, Markdown files, directories, stopword lists, font files, and optional PNG masks from paths supplied by the user. <br>
Mitigation: Point the skill only at the specific files and folders intended for analysis, and verify paths before execution. <br>
Risk: The skill writes PNG output to a user-selected directory and creates the directory when it does not exist. <br>
Mitigation: Choose the output directory deliberately and review generated files before relying on them. <br>
Risk: The skill depends on local Python packages for tokenization, image handling, and word cloud generation. <br>
Mitigation: Install dependencies from a trusted Python environment before running the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lijiahao885/wordcloud-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands; script output is a PNG image file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a timestamped wordcloud_*.png file in the selected output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
