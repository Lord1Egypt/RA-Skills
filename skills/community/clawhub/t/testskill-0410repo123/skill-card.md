## Description: <br>
Summarize URLs or files with the summarize CLI, including web pages, PDFs, images, audio, and YouTube links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to summarize URLs, local files, and YouTube links through the summarize CLI, with configurable model providers and output options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input content can be sent to configured model providers or fallback extraction services. <br>
Mitigation: Do not summarize secrets, regulated data, private documents, internal URLs, or sensitive media unless sharing that material with the configured providers is acceptable. <br>
Risk: The skill depends on a Homebrew-installed summarize CLI and user-supplied provider credentials. <br>
Mitigation: Install the CLI only from a trusted source and configure only the provider API keys required for the intended workflow. <br>


## Reference(s): <br>
- [Summarize homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/testskill-0410repo123) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON output from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports configurable summary length, token limits, extraction-only mode, provider selection, and optional fallback extraction services.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
