## Description: <br>
Analyzes YouTube notification videos for finance and trading insights, using subtitles or local transcription when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[esanle](https://clawhub.ai/user/esanle) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to inspect finance-related YouTube notifications, extract subtitles or transcripts, and summarize stock, crypto, macro, or market recommendations before any separate trade review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact workflow includes trade execution without a clear approval boundary. <br>
Mitigation: Do not allow automatic trades; require a separate explicit confirmation naming the account, symbol, side, quantity, order type, and risk before any trading action. <br>
Risk: YouTube-derived financial claims may be incomplete, misleading, or promotional. <br>
Mitigation: Treat extracted claims as untrusted research input and verify them against independent sources before using them for investment decisions. <br>
Risk: The workflow depends on local yt-dlp and whisper-cpp tools for media extraction and transcription. <br>
Mitigation: Verify local installations and model files before use, and supervise any downloaded media or generated transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/esanle/youtube-notification-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/esanle) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with shell command examples and analysis text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local transcript files and temporary logs produced during the workflow.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
