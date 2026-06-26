## Description: <br>
Track persistent topics such as stocks, companies, AI, and policy events, and monitor them continuously for recurring updates, trend tracking, structured summaries, and recent news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas-acc](https://clawhub.ai/user/lucas-acc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to define and follow long-running information topics, retrieve feeds and news-card details, search tracked signals, fetch article content, and manage topic subscriptions through the signal-track CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and reuses a YouNews API key in local OpenClaw or legacy signal-track configuration files. <br>
Mitigation: Use a dedicated YouNews API key, avoid storing unrelated credentials in a top-level OpenClaw apiKey, restrict access to the config files, and delete them when the skill is no longer needed. <br>
Risk: Tracked topics, searches, feed requests, article IDs, and follow or unfollow actions are sent to the YouNews/Sohu backend. <br>
Mitigation: Install only when this data sharing is acceptable, avoid sensitive topics where possible, and review follow or unfollow actions before running them. <br>


## Reference(s): <br>
- [ClawHub signal-track Skill](https://clawhub.ai/lucas-acc/signal-track) <br>
- [signal-track Publisher Profile](https://clawhub.ai/user/lucas-acc) <br>
- [YouNews API Base](https://younews.k.sohu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-style CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 22+, a valid YouNews API key, local configuration, and network access to the YouNews/Sohu backend.] <br>

## Skill Version(s): <br>
0.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
