## Description: <br>
Helps an agent or app turn text into audio podcast episodes, using TTS to create an episode and publish it to an RSS feed subscribable in podcast apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cast0](https://clawhub.ai/user/cast0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and app builders use this skill to create podcast episodes from supplied text, poll generation status, list episodes, and publish generated audio through a Cast0 RSS feed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted text can be turned into publicly accessible podcast episodes without a clear private review step. <br>
Mitigation: Ask for explicit user confirmation before creating or publishing an episode, and avoid secrets, private notes, internal documents, customer data, or personal material unless a separate private or draft workflow is available. <br>
Risk: The skill requires a Cast0 API key tied to a podcast. <br>
Mitigation: Store the API key in an environment variable or secret manager, avoid committing it to source control, and rotate it if it is exposed. <br>


## Reference(s): <br>
- [Cast0 API Documentation](https://api.cast0.ai/docs) <br>
- [Cast0 Dashboard](https://cast0.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/cast0/text-to-published-podcast-rss-test) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with bash and curl examples plus an endpoint table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Cast0 API key; submitted text can become a public podcast episode through the RSS feed.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
