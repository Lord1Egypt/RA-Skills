## Description: <br>
Fetches YouTube video transcripts through the Apify API with text or JSON output and optional language preference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inaor](https://clawhub.ai/user/inaor) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to retrieve YouTube transcripts from environments where direct transcript access may be blocked, then return transcript content for summarization, analysis, or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested YouTube URLs and transcript retrieval are processed through Apify and its residential proxy infrastructure. <br>
Mitigation: Use the skill only when third-party processing is acceptable, and avoid submitting private or sensitive video URLs. <br>
Risk: The skill requires an Apify API token and may incur Apify usage charges or expose billing activity. <br>
Mitigation: Use a dedicated revocable Apify token, monitor Apify usage, and rotate or revoke the token if it is no longer needed. <br>
Risk: Transcript retrieval through residential proxies may have privacy, logging, billing, or YouTube terms implications. <br>
Mitigation: Review Apify terms, YouTube terms, and organizational policy before using the skill in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/inaor/some-other-youtube) <br>
- [Apify pricing](https://apify.com/pricing) <br>
- [Apify API token settings](https://console.apify.com/account/integrations) <br>
- [YouTube Transcripts Actor](https://apify.com/karamelo/youtube-transcripts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Plain text or JSON transcript output, with Markdown setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write transcript output to a user-specified file and includes timestamps when JSON output is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
