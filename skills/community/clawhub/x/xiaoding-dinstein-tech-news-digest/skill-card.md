## Description: <br>
Generates quality-scored tech news digests from RSS, Twitter/X, GitHub, Reddit, and web search sources with Discord, email, markdown, and PDF output paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asterisk622](https://clawhub.ai/user/asterisk622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and run scheduled or on-demand technology news digests, deduplicate and score articles, and deliver reports to chat or email channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run scheduled network collection and send reports to Discord or email. <br>
Mitigation: Enable only intended delivery jobs and review channel IDs, recipient addresses, and recurring schedules before use. <br>
Risk: The skill can use GitHub credentials and a configured GitHub App private-key file. <br>
Mitigation: Use least-privilege tokens, avoid broad GitHub credentials, and verify GH_APP_KEY_FILE points only to the intended private key. <br>
Risk: The skill writes digest archives and prunes old archive files. <br>
Mitigation: Use a dedicated workspace archive directory and review retention behavior before enabling unattended runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asterisk622/xiaoding-dinstein-tech-news-digest) <br>
- [Digest prompt template](references/digest-prompt.md) <br>
- [Discord template](references/templates/discord.md) <br>
- [Email template](references/templates/email.md) <br>
- [PDF template](references/templates/pdf.md) <br>
- [Python runtime](https://www.python.org/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest text with optional HTML email, PDF report, and JSON pipeline artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Discord delivery, optional email delivery, workspace archive writes, and configurable source/topic overlays.] <br>

## Skill Version(s): <br>
3.15.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
