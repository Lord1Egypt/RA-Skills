## Description: <br>
Transform YouTube videos into Telegraph Instant View articles with visual slides and timestamped summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viticci](https://clawhub.ai/user/viticci) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to turn YouTube URLs into Telegraph article links with timestamped summaries and interleaved slides for Telegram Instant View reading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTube-derived text and images may be sent to OpenAI or summarize, catbox.moe, and Telegraph, and may become publicly accessible. <br>
Mitigation: Use only with content intended for external processing and publication; avoid private or sensitive videos. <br>
Risk: The skill can publish a Telegraph article when a user may have expected only a private YouTube summary. <br>
Mitigation: Confirm publish intent before running the script and treat this as a public article publishing workflow. <br>
Risk: Sourcing broad environment files can expose credentials beyond the Telegraph and OpenAI keys needed by the workflow. <br>
Mitigation: Use a dedicated least-privilege Telegraph token and avoid sourcing broad .env files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/viticci/youtube-instant-article) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls] <br>
**Output Format:** [Markdown guidance with shell commands; runtime script returns a Telegraph article URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Publishes YouTube-derived summaries and uploaded slides to external services; requires TELEGRAPH_TOKEN, OPENAI_API_KEY, summarize, jq, curl, and zsh.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
