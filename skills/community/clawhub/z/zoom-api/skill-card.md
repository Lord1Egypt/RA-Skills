## Description: <br>
Zoom API integration with managed OAuth for managing meetings, webinars, recordings, and user profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to access Zoom through Maton-managed OAuth for scheduling meetings, managing webinars, retrieving recordings, and reading user profile information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials and OAuth access to a connected Zoom account. <br>
Mitigation: Keep MATON_API_KEY, meeting start URLs, join links, passwords, and recording download links private. <br>
Risk: Write operations can create, modify, or delete Zoom meetings, webinars, recordings, and OAuth connections. <br>
Mitigation: Require a clear preview and user confirmation before destructive or state-changing requests. <br>
Risk: Access is mediated by Maton-managed OAuth and depends on the connected Zoom account and granted scopes. <br>
Mitigation: Install only when the publisher and Maton OAuth broker are trusted, and verify scopes before use. <br>


## Reference(s): <br>
- [Zoom ClawHub Release](https://clawhub.ai/byungkyu/zoom-api) <br>
- [Maton](https://maton.ai) <br>
- [Zoom API Documentation](https://developers.zoom.us/docs/api/) <br>
- [Zoom REST API Reference](https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/) <br>
- [Zoom Meeting API](https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#tag/Meetings) <br>
- [Zoom OAuth Scopes](https://developers.zoom.us/docs/integrations/oauth-scopes/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline HTTP examples and Python or JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a Zoom OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
