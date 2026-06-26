## Description: <br>
Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xbmchina](https://clawhub.ai/user/xbmchina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use this skill to invoke the summarize CLI for concise summaries of URLs, local files, PDFs, images, audio, and YouTube links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing and invoking an external CLI can expose users to trust and supply-chain risk. <br>
Mitigation: Verify the Homebrew tap and installed binary before use. <br>
Risk: Summarized content and prompts may be processed by configured model providers or optional extraction services. <br>
Mitigation: Avoid confidential files, private URLs, and sensitive media unless those providers and services are approved for that content. <br>
Risk: Broad or production API keys can increase blast radius if the local environment or CLI workflow is compromised. <br>
Mitigation: Use least-privilege, non-production API keys where possible and rotate credentials according to local policy. <br>


## Reference(s): <br>
- [Summarize homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/xbmchina/summarize-ai) <br>
- [Publisher profile](https://clawhub.ai/user/xbmchina) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports short, medium, long, xl, xxl, explicit character lengths, token limits, extract-only mode, and JSON output when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
