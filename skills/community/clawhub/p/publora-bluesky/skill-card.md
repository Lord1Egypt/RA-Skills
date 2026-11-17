## Description:

Post or schedule content to Bluesky using the Publora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare Publora API calls for creating or scheduling Bluesky posts, including text, images, and video-aware posting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publora API keys and Bluesky app passwords are sensitive credentials.

Mitigation: Use dedicated app passwords, avoid exposing secrets in prompts or logs, and review generated API calls before use.

Risk: Generated or scheduled post content and uploaded media are sent to Publora for processing.

Mitigation: Review content and media before publishing or scheduling, and confirm the user intends to use Publora for Bluesky posting.

Risk: Bluesky platform constraints can cause failed or altered posts, including character limits, media conversion, and ignored alt text through the API.

Mitigation: Check the documented text and media limits before posting, compress images as needed, and use the Publora dashboard when alt text is required.

## Reference(s):

- [Publora API Base URL](https://api.publora.com/api/v1)
- [Create Post Endpoint](https://api.publora.com/api/v1/create-post)
- [Upload URL Endpoint](https://api.publora.com/api/v1/get-upload-url)
- [ClawHub Skill Page](https://clawhub.ai/sergebulaev/skills/publora-bluesky)

## Skill Output:

**Output Type(s):** [API Calls, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with JavaScript and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Publora API request examples and platform limit guidance for Bluesky posts.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
