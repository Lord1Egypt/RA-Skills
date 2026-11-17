## Description:

Use when a user provides an API specification in OpenAPI or Swagger format and needs a runnable mock server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn OpenAPI or Swagger specifications into runnable mock servers with endpoint handlers, realistic mock responses, request validation, smoke-test guidance, and run instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated mock-server files may contain rough scaffold code or assumptions that do not fully match the API contract.

Mitigation: Review generated files and run endpoint smoke tests before using the mock server in a workflow.

Risk: The skill may choose common mock-server dependencies such as Prism, Mockoon, Express, or Flask without publisher-pinned trust guidance.

Mitigation: Use trusted, pinned dependencies and inspect install or run commands before executing them.

Risk: The README contains API_KEY and read/write examples that are not clearly tied to the mock-server workflow.

Mitigation: Use dummy local credentials for mock-server testing and clarify any required configuration before using real values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/wangjipeng-api-spec-to-mock-server)
- [Metadata source repository](https://github.com/MiniMax-AI/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with generated server code, inline shell commands, configuration notes, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, endpoint smoke-test results, and follow-up customization options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
