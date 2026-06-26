## Description: <br>
Remove Watermark helps agents remove light-colored text watermarks from white-background document images using local Python image processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxttt](https://clawhub.ai/user/wxttt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and document-processing agents use this skill to clean document images, screenshots, exam papers, or scanned pages by analyzing a watermark region, running a local removal script, and checking the output before relying on it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watermark removal can damage document text or alter files in ways the user did not intend. <br>
Mitigation: Keep original files, test on a preview or small sample first, and review cleaned outputs carefully before using them. <br>
Risk: The skill can be used on documents the user may not have the right to modify. <br>
Mitigation: Use it only on documents the user is authorized to edit or clean. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wxttt/remove-watermark) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local image file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script prints brightness analysis or processing status and can write cleaned image files; full-image removal requires scipy.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
