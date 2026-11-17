## Description:

Post or schedule content to Facebook Pages using the Publora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent draft Publora API requests and guidance for publishing or scheduling Facebook Page posts, including text, images, Reels, and scheduled posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward Publora API calls that publish public Facebook Page content.

Mitigation: Review the final post text, media, destination Page, and scheduled time before sending publish or schedule requests.

Risk: Publora API keys and Facebook Page IDs are sensitive operational credentials.

Mitigation: Store API keys securely, avoid exposing them in shared transcripts or code, and limit access to users authorized to manage the Page.

Risk: Facebook Page tokens may stop refreshing after permission changes, causing posting failures.

Mitigation: Reconnect the Page in the Publora dashboard when posts fail unexpectedly or after permission changes.

Risk: Unsupported media combinations or media exceeding platform limits can fail at publish time.

Mitigation: Validate media type, size, video duration, Reels limits, and mixed-media constraints before creating or uploading a post.

## Reference(s):

- [Publora API base URL](https://api.publora.com/api/v1)
- [Publora create-post endpoint](https://api.publora.com/api/v1/create-post)
- [Publora get-upload-url endpoint](https://api.publora.com/api/v1/get-upload-url)
- [ClawHub skill page](https://clawhub.ai/sergebulaev/skills/publora-facebook)

## Skill Output:

**Output Type(s):** [Guidance, Code, API Calls, Configuration]

**Output Format:** [Markdown with JavaScript fetch examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Publora platform IDs, scheduled times, content limits, media constraints, and authentication header guidance.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
