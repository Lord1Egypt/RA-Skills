## Description: <br>
Summarize URLs or files with the summarize CLI (x86_64 infrastructure supported). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[speechybubble](https://clawhub.ai/user/speechybubble) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other users use this skill to install and run the summarize CLI for summaries of URLs, local files, and YouTube links, with optional model and provider configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports a mismatch between the published skill identity and bundled metadata. <br>
Mitigation: Review the ClawHub skill page, publisher profile, and install targets before installing or delegating work to the skill. <br>
Risk: The skill can summarize local files, private URLs, or content fetched through configured providers. <br>
Mitigation: Avoid sensitive private content unless the configured AI and extraction providers are approved for that data. <br>
Risk: The skill depends on third-party npm or Homebrew install targets. <br>
Mitigation: Confirm that @speechybubble/summarize or speechybubble/tap/summarize is the intended package or formula before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/speechybubble/summarizerx64) <br>
- [speechybubble publisher profile](https://clawhub.ai/user/speechybubble) <br>
- [Summarize project homepage](https://github.com/speechybubble/summarize) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI flags for summary length, output token limits, extraction-only mode, JSON output, and optional extraction or YouTube fallback services.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
