## Description: <br>
Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmusjune](https://clawhub.ai/user/simmusjune) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to summarize web pages, local files, PDFs, images, audio, and YouTube links through the summarize CLI with configurable model, length, extraction, and JSON output options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summarized files, URLs, or media may be sent to configured AI providers or extraction services. <br>
Mitigation: Avoid confidential local files, private URLs, and proprietary media unless the selected providers are approved for that content. <br>
Risk: The skill depends on the externally installed summarize binary from a Homebrew tap. <br>
Mitigation: Install only from a trusted package source and review the package before deployment. <br>
Risk: Configured API keys may incur provider costs or grant access beyond the intended summarization task. <br>
Mitigation: Use only the API keys intended for this workflow and scope or rotate credentials according to local policy. <br>


## Reference(s): <br>
- [summarize homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/simmusjune/summarizer2) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/simmusjune) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with CLI examples; the underlying summarize command can return text or JSON summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the summarize binary and may use configured model-provider or extraction-service API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
