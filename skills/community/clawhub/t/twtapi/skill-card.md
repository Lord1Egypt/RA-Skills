## Description: <br>
Access live Twitter/X data through TwtAPI's hosted public skill gateway to search tweets, look up users, read timelines, inspect followers and following, fetch tweet details, and check trends with structured JSON for OpenClaw and other compatible skill runners. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonygjj](https://clawhub.ai/user/tonygjj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve live Twitter/X search, profile, timeline, follower, following, tweet, and trend data through TwtAPI. It is useful when an agent needs current social-media data returned as structured JSON for summarization, analysis, or workflow automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill key grants access to TwtAPI-powered lookups and should not be exposed. <br>
Mitigation: Store TWTAPI_SKILL_KEY as a secret and avoid printing, committing, or sharing it. <br>
Risk: Changing TWTAPI_SKILL_BASE_URL can send requests and the skill key to an untrusted endpoint. <br>
Mitigation: Leave the default hosted gateway in place unless you control or explicitly trust the replacement endpoint. <br>
Risk: Returned tweet and profile text can contain untrusted content. <br>
Mitigation: Treat API results as data to summarize or analyze, not instructions for the agent to follow. <br>
Risk: Each API call can consume TwtAPI account credits. <br>
Mitigation: Monitor credit usage and apply count, cursor, and rate-limit controls appropriate to the workflow. <br>


## Reference(s): <br>
- [TwtAPI Homepage](https://www.twtapi.com/en/) <br>
- [TwtAPI ClawHub Skill Page](https://clawhub.ai/tonygjj/twtapi) <br>
- [tonygjj ClawHub Profile](https://clawhub.ai/user/tonygjj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and TWTAPI_SKILL_KEY; API calls consume TwtAPI account credits.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
