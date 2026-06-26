## Description: <br>
SignNow API integration with managed OAuth for uploading documents, sending signature invites, creating templates, and managing e-signature workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to automate SignNow document, template, signing invite, folder, and webhook workflows through Maton-managed OAuth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maton API access and the SignNow OAuth connection can expose document and signing workflows. <br>
Mitigation: Install only if you trust Maton to proxy SignNow requests, protect MATON_API_KEY, and use the intended SignNow connection. <br>
Risk: Write operations can upload, send, update, delete, or create webhooks for SignNow resources. <br>
Mitigation: Review document IDs, recipients, callback URLs, target resources, and intended effects before approving any write operation. <br>
Risk: Multiple connected SignNow accounts can route a request to the wrong account. <br>
Mitigation: Include the Maton-Connection header when more than one SignNow connection exists. <br>


## Reference(s): <br>
- [ClawHub SignNow Skill](https://clawhub.ai/byungkyu/signnow) <br>
- [SignNow API Reference](https://docs.signnow.com/docs/signnow/reference) <br>
- [SignNow Developer Portal](https://www.signnow.com/developers) <br>
- [SignNow Postman Collection](https://github.com/signnow/postman-collection) <br>
- [SignNow SDKs](https://github.com/signnow) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP endpoints and Python, JavaScript, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active SignNow OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
