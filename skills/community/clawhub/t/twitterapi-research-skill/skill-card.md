## Description: <br>
General-purpose X/Twitter research agent that searches X for real-time perspectives, developer discussions, product feedback, cultural takes, breaking news, and expert opinions using twitterapi.io. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blascokoa](https://clawhub.ai/user/blascokoa) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to search X/Twitter, inspect profiles, fetch threads or individual tweets, monitor watchlists, and synthesize sourced briefings from public social discourse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, profile names, tweet IDs, and the twitterapi.io API key are sent to a third-party API provider. <br>
Mitigation: Use a dedicated prepaid twitterapi.io key, store it in TWITTERAPI_IO_KEY rather than inline commands, monitor API-credit usage, and rotate the key if exposure is suspected. <br>
Risk: Local cache, watchlist, and saved draft files may retain sensitive research topics or account monitoring data. <br>
Mitigation: Clear the cache and remove watchlist or draft files after sensitive research, and avoid sharing the skill directory without reviewing those local files. <br>
Risk: Research completeness and availability depend on twitterapi.io service behavior and the selected search filters. <br>
Mitigation: Use multiple query formulations, inspect threads and linked sources before relying on findings, and note when results are filtered by time, engagement, or page limits. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/blascokoa/twitterapi-research-skill) <br>
- [twitterapi.io](https://twitterapi.io) <br>
- [Bun runtime](https://bun.sh) <br>
- [Claude Code](https://code.claude.com) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, terminal text, or JSON depending on the selected CLI output flag] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save markdown research files and stores local cache or watchlist data when those features are used.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
