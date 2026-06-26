## Description: <br>
Post or schedule content to Threads using the Publora API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergebulaev](https://clawhub.ai/user/sergebulaev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare API calls that create or schedule Threads posts through Publora, including text, media upload, scheduling, and reply-control settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent using a Publora key can create or schedule posts for connected Threads accounts. <br>
Mitigation: Confirm the target account, post text, media, and scheduled time before allowing publish or schedule actions. <br>
Risk: Threads nested threading is temporarily unavailable, so long content may not publish as a connected reply chain. <br>
Mitigation: Keep posts under 500 characters when a single standalone post is required, or wait for Publora thread nesting support to be restored. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sergebulaev/publora-threads) <br>
- [Publora API base URL](https://api.publora.com/api/v1) <br>
- [Publora create-post endpoint](https://api.publora.com/api/v1/create-post) <br>
- [Publora upload URL endpoint](https://api.publora.com/api/v1/get-upload-url) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with JavaScript fetch examples and API parameter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Publora API base URL, API key header, Threads platform ID format, media limits, scheduling fields, and reply-control settings.] <br>

## Skill Version(s): <br>
2.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
