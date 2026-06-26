## Description: <br>
Summarize URLs or files with the summarize CLI, including web pages, PDFs, images, audio, and YouTube links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to summarize URLs, local files, PDFs, images, audio, and YouTube links through the summarize CLI. It helps produce concise or structured summaries while allowing model, length, extraction, and fallback-service options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The summarize CLI or configured model and extraction providers may receive URLs, files, document contents, or media submitted for summarization. <br>
Mitigation: Avoid passing secrets, regulated data, confidential documents, or private URLs unless the configured provider and fallback services are approved for that data. <br>
Risk: The release depends on a Homebrew tap and the summarize CLI being trustworthy in the user's environment. <br>
Mitigation: Install only after reviewing and trusting the Homebrew tap and summarize CLI package source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/test-0313-skill) <br>
- [Summarize homepage](https://summarize.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with CLI examples and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports length controls, maximum output token limits, extraction-only mode, and optional Firecrawl or Apify fallback services.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
