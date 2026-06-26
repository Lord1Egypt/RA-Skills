## Description: <br>
Post or schedule content to Bluesky using the Publora API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergebulaev](https://clawhub.ai/user/sergebulaev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to draft, publish, or schedule Bluesky posts through Publora, including text, image, and video posts within documented platform limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may publish or schedule incorrect content, media, account identifiers, or timing through Publora. <br>
Mitigation: Review the final post text, media, target Bluesky account, and scheduled time before allowing publication. <br>
Risk: Publora API keys and Bluesky app passwords can grant posting access if exposed. <br>
Mitigation: Keep the Publora API key private and use a dedicated Bluesky app password instead of the main account password. <br>


## Reference(s): <br>
- [Publora Bluesky Skill Page](https://clawhub.ai/sergebulaev/publora-bluesky) <br>
- [Publora API Base URL](https://api.publora.com/api/v1) <br>
- [Publora Create Post Endpoint](https://api.publora.com/api/v1/create-post) <br>
- [Publora Upload URL Endpoint](https://api.publora.com/api/v1/get-upload-url) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes Publora API request structure, platform identifiers, media limits, scheduling fields, and Bluesky-specific constraints.] <br>

## Skill Version(s): <br>
1.2.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
