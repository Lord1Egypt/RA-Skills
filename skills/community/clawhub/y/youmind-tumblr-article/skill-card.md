## Description: <br>
Writes and publishes Tumblr-native posts with AI, shaping topics from a YouMind knowledge base, generating long-form text or image-led posts, reviewing notes and activity, and managing the queue through a Tumblr blog connected in YouMind. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindy-youmind](https://clawhub.ai/user/mindy-youmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to draft, adapt, publish, and review Tumblr posts through a YouMind-connected Tumblr account. It supports text posts, photo posts, engagement review, follower and limit checks, and queue control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, read engagement and follower information, reorder or shuffle the queue, and delete Tumblr posts from a connected account. <br>
Mitigation: Review the skill before installation, connect only a YouMind/Tumblr account where that authority is acceptable, and verify delete or queue actions before execution. <br>
Risk: Local drafts under ~/.youmind may contain private or sensitive material. <br>
Mitigation: Review local draft storage and avoid placing confidential material in drafts unless the environment is appropriate for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindy-youmind/youmind-tumblr-article) <br>
- [YouMind Tumblr OpenAPI Reference](references/api-reference.md) <br>
- [Tumblr Publishing Pipeline](references/pipeline.md) <br>
- [Tumblr Platform DNA](references/platform-dna.md) <br>
- [Content Generation Playbook - Tumblr](references/content-generation-playbook.md) <br>
- [Content Adaptation Playbook - Tumblr](references/content-adaptation-playbook.md) <br>
- [Media Playbook - Tumblr](references/media-playbook.md) <br>
- [Engagement Playbook - Tumblr](references/engagement-playbook.md) <br>
- [YouMind API Keys](https://youmind.com/settings/api-keys?utm_source=youmind-tumblr-article) <br>
- [YouMind Connector Settings](https://youmind.com/settings/connector?utm_source=youmind-tumblr-article) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated Tumblr post text, simple HTML drafts, and API-backed result links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish, read engagement data, manage queues, and save local drafts under ~/.youmind when configured with YouMind credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
