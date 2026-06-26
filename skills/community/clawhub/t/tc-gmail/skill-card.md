## Description: <br>
Read, send, and manage Gmail emails, threads, labels, and drafts via Gmail API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to Gmail for mailbox search, message retrieval, email sending, label management, and draft workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent Gmail OAuth access can expose sensitive mailbox data or allow email and label changes. <br>
Mitigation: Use a dedicated OAuth client with the narrowest Gmail scopes possible, protect the refresh token like a password, and revoke it when finished. <br>
Risk: The skill can send email, include attachments, create drafts, and change mailbox labels. <br>
Mitigation: Require final human review before any email is sent, attachment is included, draft is created, or mailbox labels are changed. <br>
Risk: Server evidence reports unavailable import provenance and a suspicious security verdict. <br>
Mitigation: Install only when the publisher is trusted and the requested Gmail access is acceptable for the deployment. <br>


## Reference(s): <br>
- [Gmail API documentation](https://developers.google.com/gmail/api) <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/tc-gmail) <br>
- [Publisher profile](https://clawhub.ai/user/terrycarter1985) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Gmail OAuth credentials and Google API client packages.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
