## Description:

Post or schedule Instagram images, reels, stories, and carousels through the Publora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and social media teams use this skill to let an agent prepare Publora API calls for publishing or scheduling Instagram media posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Publora API key can authorize Instagram publishing or scheduling actions.

Mitigation: Store the API key securely, avoid exposing it in prompts or logs, and provide it only when the agent is expected to prepare Publora requests.

Risk: Generated requests can create public or scheduled Instagram posts.

Mitigation: Review captions, platform targets, scheduled times, and media files before sending requests to Publora.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sergebulaev/skills/publora-instagram)
- [Publora API base URL](https://api.publora.com/api/v1)
- [Publora create-post endpoint](https://api.publora.com/api/v1/create-post)
- [Publora get-upload-url endpoint](https://api.publora.com/api/v1/get-upload-url)

## Skill Output:

**Output Type(s):** [Code, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline code examples and API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JavaScript or Python examples for creating posts, requesting upload URLs, and uploading media.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
