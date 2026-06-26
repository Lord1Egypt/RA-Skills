## Description: <br>
Pull tweets, threads, articles, and replies from X/Twitter. FxTwitter API primary (free), Grok x_search fallback (paid). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sanjeevneo](https://clawhub.ai/user/sanjeevneo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use xpull to retrieve X/Twitter posts, threads, replies, article content, and search results through FxTwitter or xAI Grok-backed commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tweet URLs and search queries are sent to external FxTwitter or xAI APIs. <br>
Mitigation: Use inputs appropriate for those services and avoid submitting sensitive or restricted content. <br>
Risk: Grok x_search usage requires an xAI API key and may incur usage costs. <br>
Mitigation: Set XAI_API_KEY only when Grok features are needed and use GROK_DAILY_CAP to limit daily calls. <br>
Risk: The Grok script writes a local .grok-state.json file to track daily call limits. <br>
Mitigation: Run it in a workspace where local state files are acceptable and reset the state file only when deliberately resetting usage tracking. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sanjeevneo/xpull) <br>
- [Project repository](https://github.com/sanjeevneo/xpull) <br>
- [xAI Console](https://console.x.ai) <br>
- [FxTwitter API endpoint](https://api.fxtwitter.com) <br>
- [xAI Responses API endpoint](https://api.x.ai/v1/responses) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts return JSON to stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Grok features require XAI_API_KEY; GROK_DAILY_CAP can limit daily Grok calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
