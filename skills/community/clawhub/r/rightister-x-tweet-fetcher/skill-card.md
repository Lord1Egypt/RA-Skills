## Description: <br>
Fetches X/Twitter tweets, replies, timelines, X Lists, mentions, Chinese platform content, Google search results, and tweet growth signals for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rightister](https://clawhub.ai/user/rightister) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve social-media content and monitoring signals from X/Twitter and supported Chinese platforms without paid platform APIs. It is suited for structured content extraction, timeline review, mention monitoring, search, and tweet growth analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some execution paths use session cookies, SSH, or router command queues. <br>
Mitigation: Prefer basic fetch paths, run browser automation in an isolated environment, avoid primary-account cookies, and use SSH or router modes only with hosts and agent files you control. <br>
Risk: The release was classified as suspicious by the server security scan because it is broader than a simple tweet fetcher. <br>
Mitigation: Review enabled commands before installation and limit use to the specific fetching or monitoring features needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rightister/rightister-x-tweet-fetcher) <br>
- [Publisher profile](https://clawhub.ai/user/rightister) <br>
- [Camoufox](https://camoufox.com) <br>
- [FxEmbed](https://github.com/FxEmbed/FxEmbed) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Basic tweet fetching has no external dependency; replies, timelines, search, and most Chinese platform fetches may require Camofox on localhost.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
