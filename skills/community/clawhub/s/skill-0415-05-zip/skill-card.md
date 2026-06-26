## Description: <br>
Summarize URLs or files with the summarize CLI, including web pages, PDFs, images, audio, and YouTube links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to summarize URLs, local files, and media through the summarize CLI. It is useful when a workflow needs concise text or machine-readable summaries from web pages, documents, images, audio, or YouTube content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted URLs, files, or media may be processed by external model or extraction providers. <br>
Mitigation: Do not submit confidential files, private URLs, secrets, or regulated data unless the configured providers are approved for that data. <br>
Risk: Optional Firecrawl and Apify fallbacks can route extraction or YouTube processing to additional third-party services. <br>
Mitigation: Leave optional fallbacks disabled unless intentionally configured and approved. <br>
Risk: The skill depends on the Homebrew-installed summarize CLI. <br>
Mitigation: Install only if the summarize Homebrew package and its configured providers are trusted. <br>


## Reference(s): <br>
- [Summarize homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skill-0415-05-zip) <br>
- [Publisher profile](https://clawhub.ai/user/yinwuzhe) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; summaries may be plain text or JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the summarize binary and a configured model provider API key for normal operation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
