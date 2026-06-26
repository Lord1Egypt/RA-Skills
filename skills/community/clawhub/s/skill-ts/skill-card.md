## Description: <br>
Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tranhuilee](https://clawhub.ai/user/tranhuilee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate summarize CLI commands for summarizing web pages, local files, media, and YouTube links with a chosen model provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external summarize CLI and Homebrew tap. <br>
Mitigation: Install it only from sources you trust and review the CLI before using it in sensitive environments. <br>
Risk: Summarizing private files or URLs can send content to configured model or extraction services. <br>
Mitigation: Avoid confidential inputs unless the selected provider and extraction service are approved for that data. <br>
Risk: Provider credentials and optional extraction-service tokens can enable paid API usage. <br>
Mitigation: Set only the API keys required for the intended provider and monitor usage and billing. <br>


## Reference(s): <br>
- [Summarize homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/tranhuilee/skill-ts) <br>
- [Publisher profile](https://clawhub.ai/user/tranhuilee) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model-provider API key setup, summarize CLI flags, and optional JSON-output guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
