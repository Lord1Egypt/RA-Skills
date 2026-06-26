## Description: <br>
Render structured data as hosted web pages and create hosted forms for surveys, RSVPs, feedback, and other structured data using the RenderKit API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antoinedc](https://clawhub.ai/user/antoinedc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to generate hosted visual pages from structured content and create hosted forms for collecting responses through RenderKit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may send selected page content, form definitions, and submissions to RenderKit. <br>
Mitigation: Avoid collecting secrets or sensitive personal data unless provider terms, consent, and data handling requirements have been reviewed. <br>
Risk: The skill requires a RenderKit API key in the agent environment. <br>
Mitigation: Store the API key only in the intended environment variable and avoid exposing it in prompts, shared logs, or rendered content. <br>
Risk: Closing a live form can affect ongoing data collection. <br>
Mitigation: Confirm form IDs before issuing close or delete requests. <br>


## Reference(s): <br>
- [RenderKit homepage](https://renderkit.live) <br>
- [RenderKit API documentation](https://renderkit.live/docs.md) <br>
- [ClawHub skill page](https://clawhub.ai/antoinedc/renderkit) <br>
- [Publisher profile](https://clawhub.ai/user/antoinedc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl command examples and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and the RENDERKIT_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
