## Description: <br>
Summarizes URLs, PDFs, images, audio, and YouTube links through a configurable CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seeu1688](https://clawhub.ai/user/seeu1688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to summarize web pages, local files, media, and YouTube content with selectable model providers and output controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided files, private URLs, or media may be sent to configured model providers or optional extraction services. <br>
Mitigation: Avoid confidential inputs unless the selected provider and optional Firecrawl or Apify services are approved for that data. <br>
Risk: The skill requires API credentials for model providers and optional extraction services. <br>
Mitigation: Set only the API keys required for the current workflow and avoid sharing unnecessary credentials with the runtime environment. <br>
Risk: Installation depends on a third-party Homebrew tap. <br>
Mitigation: Review the Homebrew tap before installation when it is not already trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seeu1688/summarize-xhs) <br>
- [Summarize homepage](https://summarize.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Text or JSON summaries, with Markdown guidance and inline shell commands for setup and use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summary length, output token limit, extraction mode, provider model, and optional fallback extraction services are configurable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
