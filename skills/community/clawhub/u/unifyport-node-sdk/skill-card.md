## Description:

Use when maintaining or using the UnifyPort Node.js SDK; covers the Device API client, public contract, generated code, errors, retries, and the new API workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unifyport](https://clawhub.ai/user/unifyport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate the public @unifyport/sdk-node package into Node.js or TypeScript projects, or to maintain the SDK's Device API client, public contract, generated code, errors, retries, and tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials could be exposed if pasted into chat, source files, logs, tool inputs, or committed configuration.

Mitigation: Read the base URL and API key from runtime environment variables, do not request or print real keys, and keep credentials out of generated files and logs.

Risk: Live Device API requests can affect approved test or deployment environments if run only to validate an installation.

Mitigation: Prefer type checking and mocked transport tests; perform live calls only when explicitly requested and when credentials are supplied through an approved runtime environment.

Risk: Manual path, header, retry, or contract changes can bypass the SDK's typed safety boundaries.

Mitigation: Use typed SDK operations, client-managed authentication headers, approved public API schemas, and explicit retry classification for sensitive or side-effecting operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unifyport/skills/unifyport-node-sdk)
- [@unifyport/sdk-node npm package](https://www.npmjs.com/package/@unifyport/sdk-node)
- [UnifyPort publisher profile](https://clawhub.ai/user/unifyport)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include install commands, Node.js or TypeScript code snippets, configuration guidance, and verification commands; live API calls require user-approved runtime credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
