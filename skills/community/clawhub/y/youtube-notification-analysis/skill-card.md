## Description:

Analyze YouTube notifications for investment and trading insights by extracting financial video content, retrieving subtitles or transcriptions, summarizing recommendations, and optionally handing trade execution to a trading skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[esanle](https://clawhub.ai/user/esanle)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to review investment-related YouTube notifications, extract or transcribe video content, and summarize stock, crypto, macro finance, and market-trend recommendations. The workflow may connect those recommendations to a separate trading skill, so trade actions require independent review and approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted YouTube financial content may be converted into trading recommendations or trade execution steps without a clear approval checkpoint.

Mitigation: Require explicit review and approval of the asset, side, quantity, account, price, and risk before every order, and keep trade execution disabled unless a separate trading workflow enforces those checks.

Risk: The skill accesses YouTube notification context and analyzes financial videos.

Mitigation: Install and run it only when that notification access and financial-content analysis are intended for the user or agent session.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell command snippets and investment-analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save logs under /tmp/youtube_investment_*.log and may invoke browser actions, yt-dlp, whisper-cpp, and a separate trading skill when available.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
