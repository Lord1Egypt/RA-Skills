## Description:

Pull tweets, threads, articles, and replies from X/Twitter. FxTwitter API primary (free), Grok x_search fallback (paid).

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanjeevneo](https://clawhub.ai/user/sanjeevneo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve X/Twitter posts, author threads, replies, and search results for analysis or summarization workflows. FxTwitter-backed fetches need no credential, while Grok-backed thread, reply, and search features require an xAI API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested X/Twitter URLs or search queries are sent to FxTwitter or xAI.

Mitigation: Use the skill only for content that may be shared with those services, and avoid submitting sensitive private queries or URLs.

Risk: Grok features require XAI_API_KEY and may read it from the current working directory .env file.

Mitigation: Use an xAI-scoped key and keep unrelated secrets out of the working directory .env file.

Risk: Grok x_search usage can incur paid API charges.

Mitigation: Set and monitor GROK_DAILY_CAP before enabling Grok-backed thread, reply, or search workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanjeevneo/skills/xpull)
- [Publisher profile](https://clawhub.ai/user/sanjeevneo)
- [Repository declared in skill metadata](https://github.com/sanjeevneo/xpull)
- [xAI Console](https://console.x.ai)
- [FxTwitter API endpoint](https://api.fxtwitter.com)
- [xAI Responses API endpoint](https://api.x.ai/v1/responses)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; scripts emit JSON to stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [FxTwitter fetches call api.fxtwitter.com without credentials; Grok features call api.x.ai with XAI_API_KEY and use GROK_DAILY_CAP for a daily usage cap.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
