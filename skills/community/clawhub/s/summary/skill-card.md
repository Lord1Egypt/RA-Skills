## Description: <br>
Summarize URLs or files with the summarize CLI, including web pages, PDFs, images, audio, and YouTube links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anbring](https://clawhub.ai/user/anbring) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and content reviewers use this skill to invoke a local summarize CLI for concise summaries of URLs, files, media, and YouTube links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted files, URLs, images, audio, or YouTube content may be sent to external AI or extraction providers. <br>
Mitigation: Use only approved model and extraction providers, and avoid confidential, regulated, or private inputs unless those providers are approved for that data. <br>
Risk: The skill depends on the Homebrew tap and installed summarize binary declared in metadata. <br>
Mitigation: Install only when you trust the Homebrew tap and can verify the installed CLI before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anbring/summary) <br>
- [Summarize homepage](https://summarize.sh) <br>
- [Publisher profile](https://clawhub.ai/user/anbring) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce machine-readable JSON when the summarize CLI is run with its JSON flag.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
