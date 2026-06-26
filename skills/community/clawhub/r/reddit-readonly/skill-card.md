## Description: <br>
Browse and search Reddit in read-only mode using public JSON endpoints for subreddit listings, post search, comment threads, and permalink shortlists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buksan1950](https://clawhub.ai/user/buksan1950) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to research public Reddit discussions, inspect threads for context, and build shortlists of relevant permalinks for manual review or reply. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and returned Reddit content can include sensitive or untrusted public text. <br>
Mitigation: Avoid placing sensitive personal information in Reddit queries and review returned content before relying on it. <br>
Risk: Reddit public endpoints may rate limit, timeout, or return HTML instead of JSON. <br>
Mitigation: Use small result limits first and reduce request rate with the documented delay and timeout environment variables. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buksan1950/reddit-readonly) <br>
- [Output schema](artifact/references/OUTPUT_SCHEMA.md) <br>
- [Reddit public site](https://www.reddit.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [JSON command output with Markdown summaries and permalink shortlists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return standardized ok/data or ok/error JSON and include Reddit permalinks in user-facing results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
