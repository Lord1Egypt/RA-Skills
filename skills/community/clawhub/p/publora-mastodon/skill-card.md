## Description:

Post or schedule content to Mastodon using the Publora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to draft, publish, or schedule Mastodon posts through Publora, including text posts and selected media uploads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help publish or schedule Mastodon content through Publora.

Mitigation: Verify the target account, platform ID, scheduled time, and final post content before sending requests.

Risk: Publora API keys are required for publishing operations.

Mitigation: Keep the Publora API key private and avoid placing real keys in shared prompts, logs, or examples.

Risk: Media upload workflows may expose unintended local files.

Mitigation: Upload only files the user explicitly selected for the Mastodon post.

## Reference(s):

- [Publora API Base URL](https://api.publora.com/api/v1)
- [Publora Mastodon Skill Page](https://clawhub.ai/sergebulaev/skills/publora-mastodon)
- [Publisher Profile](https://clawhub.ai/user/sergebulaev)

## Skill Output:

**Output Type(s):** [guidance, code, API Calls, configuration]

**Output Format:** [Markdown with JavaScript and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include post content, platform IDs, scheduled timestamps, and media upload steps.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
