## Description: <br>
Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to summarize web pages, local documents, media files, and YouTube links through the summarize CLI. It is suited for workflows that need concise text or JSON summaries from supported external and local inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external CLI installed from a Homebrew tap and on SkillBoss API Hub. <br>
Mitigation: Install only after confirming the Homebrew tap and external service are trusted for the intended environment. <br>
Risk: Summarizing confidential files, private URLs, or sensitive transcripts may send content to an external service and downstream model providers. <br>
Mitigation: Avoid sensitive inputs unless the external processing path is approved for that data. <br>


## Reference(s): <br>
- [summarize homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/toby-summarize) <br>
- [Publisher profile](https://clawhub.ai/user/tobeyrebecca) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports summary length controls, JSON output, extraction-only mode, and optional web or YouTube fallback behavior through the configured external API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
