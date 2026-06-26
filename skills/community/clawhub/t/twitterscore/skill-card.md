## Description: <br>
Research, analyze, and track Twitter influence with the TwitterScore.io API, including account scores, follower analysis, growth history, and account comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NikolayBohdanov](https://clawhub.ai/user/NikolayBohdanov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and social intelligence teams use this skill to query TwitterScore.io for Twitter account influence, follower composition, follower growth, and bulk account comparisons. The skill is useful when an agent needs to propose CLI commands, API-backed analysis steps, or export workflows for TwitterScore data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried Twitter account names, IDs, and target lists are sent to TwitterScore.io. <br>
Mitigation: Avoid submitting confidential target lists unless that disclosure is acceptable for the workflow. <br>
Risk: The workflow requires a TwitterScore API key and may expose it if passed directly on shared command lines. <br>
Mitigation: Use a dedicated revocable API key and prefer environment or agent configuration storage over command-line arguments. <br>
Risk: The skill depends on the local twitterscore CLI and the external TwitterScore.io API. <br>
Mitigation: Install and run it only in environments where those tools and services are trusted. <br>


## Reference(s): <br>
- [ClawHub TwitterScore release](https://clawhub.ai/NikolayBohdanov/twitterscore) <br>
- [TwitterScore API documentation](https://twitterscore.gitbook.io/twitterscore/developers/api-documentation) <br>
- [TwitterScore API pricing](https://twitterscore.io/api/prices?i=9720) <br>
- [TwitterScore API base URL](https://twitterscore.io/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, CSV] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON or CSV result formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TwitterScore API key and sends queried account names, IDs, and target lists to TwitterScore.io.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
