## Description: <br>
Summarize URLs or files with the summarize CLI, including web pages, PDFs, images, audio files, and YouTube videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[164149043](https://clawhub.ai/user/164149043) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to produce concise summaries from URLs, local documents, media files, and YouTube videos through the summarize CLI. It is useful when an agent needs repeatable command examples for summary length, output format, and saving summaries to files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URLs and files passed to the summarize CLI may contain sensitive or private content. <br>
Mitigation: Use the skill only with inputs that are appropriate for processing by the installed summarize CLI. <br>
Risk: The skill depends on an external CLI installed from a Homebrew tap. <br>
Mitigation: Verify that the Homebrew tap and summarize CLI are the intended tools before installation and use. <br>
Risk: The --output option can save summaries to unintended locations. <br>
Mitigation: Choose output paths deliberately and review generated files before sharing or committing them. <br>


## Reference(s): <br>
- [Summarize CLI homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/164149043/summarize-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text, markdown, json] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI outputs can be text, Markdown, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports summary length selection, output format selection, and writing summaries to a chosen file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
