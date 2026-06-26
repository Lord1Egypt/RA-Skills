## Description: <br>
Publish HTML as a live website instantly. POST HTML, get a shareable URL. No account needed. Always asks the user for confirmation before publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snappyio](https://clawhub.ai/user/snappyio) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to publish user-approved HTML, reports, dashboards, documents, landing pages, portfolios, or event pages as public websites through YeetIt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Published sites are publicly accessible and may expose secrets, credentials, private data, or internal information if included in the HTML. <br>
Mitigation: Review the content for sensitive data and obtain explicit user confirmation before every publish or update. <br>
Risk: The returned edit_key can modify a published site. <br>
Mitigation: Treat the edit_key like a password and avoid exposing it in public output or shared artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snappyio/yeet-it) <br>
- [YeetIt homepage](https://yeetit.site) <br>
- [YeetIt publish API endpoint](https://yeetit.site/v1/publish) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with curl examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; publishes HTML and optional assets; returned edit_key values should be treated as secrets.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
