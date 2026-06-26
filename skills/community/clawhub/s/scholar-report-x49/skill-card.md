## Description: <br>
Scholar Report generates asynchronous AI-powered academic literature review reports through the Scholar API, with inline citations, paper evidence, and downloadable Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wahahaaaa123](https://clawhub.ai/user/wahahaaaa123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and researchers use this skill to create, poll, and download structured literature review reports for research questions, with optional filters for language, publication years, and paper types. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research questions and report topics are sent to the third-party Scholar API at scholar.x49.ai. <br>
Mitigation: Use only topics suitable for third-party processing, and avoid confidential or unpublished research unless the service's data handling is understood. <br>
Risk: The skill includes a shared built-in bearer token. <br>
Mitigation: Prefer setting SCHOLAR_API_KEY to a user-controlled key before use. <br>
Risk: Downloaded reports can persist generated research content in the workspace. <br>
Mitigation: Save Markdown reports only when persistence is intended, and review generated citations before relying on them. <br>


## Reference(s): <br>
- [Scholar API documentation](https://scholar.x49.ai/docs?section=api-keys) <br>
- [Scholar API base URL](https://scholar.x49.ai/api/v1) <br>
- [ClawHub skill release page](https://clawhub.ai/wahahaaaa123/scholar-report-x49) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples; downloaded reports are raw Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCHOLAR_API_KEY or a built-in free bearer token; report generation is asynchronous and uses polling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
