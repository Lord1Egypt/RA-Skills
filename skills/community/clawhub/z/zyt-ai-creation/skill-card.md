## Description:

Use Chanjing AI creation APIs to submit image or video generation tasks across multiple models, inspect task status, poll async results, and explicitly download generated assets when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyuting214](https://clawhub.ai/user/zuoyuting214)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to submit Chanjing image or video generation jobs, check task history and task status, poll asynchronous results, and download generated media only when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials and cached access tokens are used for Chanjing AI creation APIs and could be exposed if local configuration is mishandled.

Mitigation: Keep the Chanjing credentials directory private, use credentials intended for this workflow, and prefer limited-scope or test credentials when evaluating the skill.

Risk: The configurable API base could send credentials or requests to an unsafe endpoint.

Mitigation: Use the default Chanjing HTTPS endpoint unless a trusted Chanjing-controlled endpoint is explicitly required.

Risk: Submitting, listing, and polling generation tasks can consume API quota and reveal task history.

Mitigation: Review requested operations before execution and run them only in accounts where this access is intended.

## Reference(s):

- [Chanjing Open API base](https://open-api.chanjing.cc)
- [Chanjing Open API login](https://www.chanjing.cc/openapi/login)
- [Skill reference](artifact/reference.md)
- [Skill examples](artifact/examples.md)
- [ClawHub skill page](https://clawhub.ai/zuoyuting214/skills/zyt-ai-creation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return task identifiers, task detail JSON, remote output URLs, or local file paths when downloads are explicitly requested.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
