## Description: <br>
Generates Fu Sheng-style Chinese article text and an optional cover image, then publishes the post to a Tumblr blog after collecting topic and audience inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgx-00](https://clawhub.ai/user/lgx-00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators or social media operators use this skill to draft Chinese thought-leadership posts, optionally generate cover art, and publish the result to Tumblr from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports embedded account credentials. <br>
Mitigation: Replace the credentials with user-controlled secrets before use and revoke any credentials shipped in the artifact. <br>
Risk: The release evidence reports that the skill can publish public Tumblr posts without a clear user-controlled approval flow. <br>
Mitigation: Review the generated content and destination blog before publishing, and prefer a version that defaults to draft or preview with explicit final approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lgx-00/tumblr-auto-post) <br>
- [Publisher profile](https://clawhub.ai/user/lgx-00) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, API calls] <br>
**Output Format:** [Console text with generated article content and a returned Tumblr post URL; optional JPEG cover image file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish directly to Tumblr; requires python3, OAuth credentials, and uv plus GEMINI_API_KEY for cover image generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
