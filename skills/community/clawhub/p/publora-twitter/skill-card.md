## Description:

Post or schedule content to X (Twitter) using the Publora API when the user wants to tweet, schedule a tweet, or post a thread via Publora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

External users, social media managers, and developers use this skill to prepare Publora API requests for publishing, scheduling, or threading posts on X/Twitter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publora requests can publish or schedule public X/Twitter content.

Mitigation: Review post content, target platform ID, attached media, and schedule time before allowing any request that would publish publicly.

Risk: The Publora API key is a sensitive credential.

Mitigation: Keep the key out of shared prompts, logs, and committed files, and use it only for intended Publora API requests.

Risk: Plan requirements and platform limits can cause posting failures or unexpected thread/media behavior.

Mitigation: Confirm the account has Pro or Premium access and check text, media, threading, and 120-second video limits before posting or scheduling.

## Reference(s):

- [Publora Twitter skill page](https://clawhub.ai/sergebulaev/skills/publora-twitter)
- [Publora API base URL](https://api.publora.com/api/v1)
- [Publora create-post endpoint](https://api.publora.com/api/v1/create-post)

## Skill Output:

**Output Type(s):** [Guidance, Code, API Calls, Configuration]

**Output Format:** [Markdown with JavaScript fetch examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Publora API key and a twitter-{userId} platform ID; review content before publishing or scheduling.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
