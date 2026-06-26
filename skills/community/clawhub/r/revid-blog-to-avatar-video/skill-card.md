## Description: <br>
Turn a blog post URL into a talking-head avatar video: the avatar reads a summarized script of the post against a clean background. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[api00](https://clawhub.ai/user/api00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content automation users use this skill to turn blog or article URLs into talking-head avatar videos by calling the Revid API, polling the render status, and returning the generated video URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends blog content and avatar image links to Revid. <br>
Mitigation: Use it only when the user trusts Revid with those inputs and has authorization to submit the referenced content. <br>
Risk: The workflow requires REVID_API_KEY, a sensitive credential. <br>
Mitigation: Treat REVID_API_KEY as a secret and avoid exposing it in logs, committed files, or shared command output. <br>
Risk: Avatar images or likenesses may involve rights, consent, or access-control concerns. <br>
Mitigation: Use only avatar images, character IDs, and source URLs the user is authorized to use, and avoid private or access-controlled URLs unless explicitly permitted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/api00/revid-blog-to-avatar-video) <br>
- [Publisher profile](https://clawhub.ai/user/api00) <br>
- [Revid render API endpoint](https://www.revid.ai/api/public/v3/render) <br>
- [Revid status API endpoint](https://www.revid.ai/api/public/v3/status?pid=$PID) <br>
- [Revid consistent characters API endpoint](https://www.revid.ai/api/public/v3/consistent-characters) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with HTTP examples, JSON payloads, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns or guides the agent to return a Revid videoUrl after render completion.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
