## Description: <br>
Post to social media via VibePost API. Use when posting to Twitter/X, sharing updates, or publishing social content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and agents use this skill to publish reviewed social updates to Twitter/X or another specified social platform through the VibePost API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish live external social posts using an embedded credential with unclear account control. <br>
Mitigation: Install only if the publisher and VibePost service are trusted; prefer a version that uses your own scoped API key or OAuth setup. <br>
Risk: A user or prompt injection could pressure the agent to post without clear consent. <br>
Mitigation: Require a separate explicit confirmation of the exact post text and destination before executing any publish command. <br>
Risk: Local files or sensitive data could be exfiltrated through public post content. <br>
Mitigation: Do not read local files into posts; only publish text the user directly provides and approves. <br>
Risk: Content could be sent to an unintended platform or audience. <br>
Mitigation: Post only to the user-specified platform and require explicit approval before cross-posting or bulk posting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/social-poster-hardened) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/social-poster) <br>
- [VibePost posting API endpoint](https://vibepost-jpaulgrayson.replit.app/api/quack/post) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Publishes externally after explicit confirmation of the exact post text and destination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
