## Description: <br>
Screenshot Tool captures webpages and converts PPT, Word, Excel, and PDF documents into high-resolution PNG images while preserving layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[834948655](https://clawhub.ai/user/834948655) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation authors, and operations teams use this skill to capture full or partial webpages and turn office documents or PDFs into PNG images for review, presentation, or publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted URLs or filenames may cause unintended local shell commands when the bundled scripts invoke subprocesses through the shell. <br>
Mitigation: Use only trusted URLs and filenames, run the skill in a sandbox or disposable environment, and update scripts to call subprocess.run with argument lists and shell=False before broader deployment. <br>
Risk: Screenshots and converted document images may expose sensitive content from logged-in pages or private files. <br>
Mitigation: Review inputs before capture, store outputs in access-controlled locations, and delete generated images when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/834948655/screenshot-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG image files with Markdown-style command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Document conversion defaults to 300 DPI PNG output; webpage screenshots use agent-browser and may be full-page or viewport captures.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
