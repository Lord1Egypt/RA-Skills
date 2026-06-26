## Description: <br>
Turn any markdown into a shareable web page via md.page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maypaz](https://clawhub.ai/user/maypaz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to publish selected Markdown as a shareable md.page URL after reviewing the content for secrets or confidential material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive, personal, confidential, or credential-like Markdown could be published to a shareable URL. <br>
Mitigation: Review content before publishing and do not publish files or generated text containing secrets, credentials, private keys, or confidential material without explicit user confirmation. <br>
Risk: The resulting md.page URL is shareable with anyone who has the link. <br>
Mitigation: Treat published pages as externally shareable and avoid publishing material that should remain private. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maypaz/publish-to-mdpage) <br>
- [md.page](https://md.page) <br>
- [md.page publish API](https://md.page/api/publish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown response with a shareable URL and relevant expiration or error guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads Markdown content to md.page; generated links expire in 24 hours according to the skill artifact.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
