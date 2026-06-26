## Description: <br>
Fetch and paginate Twitter/X data using twitterapi.io for tweets, user profiles, timelines, replies, quote tweets, thread context, mentions, and advanced search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ropl-btc](https://clawhub.ai/user/ropl-btc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform read-only Twitter/X data retrieval through the twitterapi.io CLI without writing raw API calls for common tweet, user, timeline, reply, quote, thread, mention, and search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed if users place real credentials directly in shared commands, logs, or transcripts. <br>
Mitigation: Use environment-variable or secret-manager injection and avoid sharing command history or transcripts that contain credentials. <br>
Risk: The preferred Git install command tracks the repository head, so future upstream changes could alter behavior after release review. <br>
Mitigation: Pin the Git revision when installing in controlled environments. <br>
Risk: The CLI stores local configuration for authentication. <br>
Mitigation: Keep local config files protected and review access to the user config directory on shared systems. <br>


## Reference(s): <br>
- [twitterapi.io official docs links](references/links.md) <br>
- [twitterapi-io-cli package repository](https://github.com/ropl-btc/twitterapi-io-cli) <br>
- [twitterapi.io documentation index](https://docs.twitterapi.io/llms.txt) <br>
- [twitterapi.io authentication](https://docs.twitterapi.io/authentication) <br>
- [twitterapi.io advanced search](https://docs.twitterapi.io/api-reference/endpoint/tweet_advanced_search) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI defaults to compact JSON and supports raw endpoint payloads when requested.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
