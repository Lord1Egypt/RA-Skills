## Description: <br>
Post or schedule content to Mastodon using the Publora API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergebulaev](https://clawhub.ai/user/sergebulaev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and social media operators use this skill to draft, publish, or schedule Mastodon posts through Publora, including text, images, and video for the mastodon.social instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent post or schedule public, federated Mastodon content through a third-party API. <br>
Mitigation: Review text and media before sending, avoid secrets or private personal data, and confirm the intended account and schedule. <br>
Risk: Publora API keys grant posting capability and are sensitive credentials. <br>
Mitigation: Store the API key securely, avoid exposing it in prompts or generated content, and rotate it if disclosure is suspected. <br>
Risk: Current Publora support is limited to the mastodon.social instance. <br>
Mitigation: Confirm the target account uses the supported instance before attempting to publish or schedule posts. <br>


## Reference(s): <br>
- [Publora Mastodon skill page](https://clawhub.ai/sergebulaev/publora-mastodon) <br>
- [Publora API base URL](https://api.publora.com/api/v1) <br>
- [Publora create-post endpoint](https://api.publora.com/api/v1/create-post) <br>
- [Publora get-upload-url endpoint](https://api.publora.com/api/v1/get-upload-url) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API calls, Configuration] <br>
**Output Format:** [Markdown with JavaScript and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Mastodon post content, scheduling payloads, media upload steps, endpoint details, and platform limits.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
