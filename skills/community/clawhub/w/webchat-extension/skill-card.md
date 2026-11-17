## Description:

Deploys a Chromium browser extension and local Express/SSE backend that let users select or copy webpage text and stream contextual answers from CodeBuddy AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noaheleven](https://clawhub.ai/user/noaheleven)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to deploy, configure, and package a browser-based webpage chat assistant. The deployed extension helps users carry selected or copied webpage context into CodeBuddy AI conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and persist selected or copied webpage and clipboard text, which may include sensitive data.

Mitigation: Require explicit user confirmation before adding clipboard content, avoid use on sensitive pages, and review stored conversation/context data before sharing or packaging.

Risk: The local AI backend uses local CodeBuddy login or API-key credentials and was flagged as lacking sufficient access control.

Mitigation: Bind the backend to loopback only, add backend authentication, keep API keys only in local environment files, and exclude credentials from release archives.

Risk: The backend CORS and browser-panel message handling may allow unintended local access if left broad.

Mitigation: Restrict CORS to expected extension origins, check message sources, and keep browser permissions scoped to the extension workflow.

Risk: The release depends on a local CodeBuddy CLI, a Windows protocol handler, and npm dependencies that must be trusted and current.

Mitigation: Install dependencies from trusted sources, update dependency versions before sensitive use, review protocol-handler registration, and verify the generated launcher path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noaheleven/skills/webchat-extension)
- [Publisher profile](https://clawhub.ai/user/noaheleven)
- [Deployment and troubleshooting guide](references/deploy-guide.md)
- [CodeBuddy](https://www.codebuddy.cn)
- [CodeBuddy API console](https://copilot.tencent.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment instructions and file-generation steps for a Chromium extension and local Node.js backend.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
