## Description: <br>
Guides developers through adding You.com web search, AI agent, and content extraction tools to Vercel AI SDK applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EdwardIrby](https://clawhub.ai/user/EdwardIrby) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to integrate @youdotcom-oss/ai-sdk-plugin tools into Vercel AI SDK generateText() and streamText() workflows, including Node.js, Next.js, Express.js, and React examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The npm package dependency could change after integration. <br>
Mitigation: Review and pin @youdotcom-oss/ai-sdk-plugin to an appropriate version before installing it in production applications. <br>
Risk: You.com API keys could be exposed if written directly into source files or committed. <br>
Mitigation: Store the API key in an environment variable or secret manager and avoid committing secrets. <br>
Risk: Prompts, private URLs, or regulated data may be sent through added web tools. <br>
Mitigation: Avoid sending sensitive data unless the application requirements and provider agreements permit it. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/EdwardIrby/ydc-ai-sdk-integration) <br>
- [Package README](https://github.com/youdotcom-oss/dx-toolkit/tree/main/packages/ai-sdk-plugin) <br>
- [Vercel AI SDK Docs](https://ai-sdk.dev/docs) <br>
- [You.com API keys](https://you.com/platform/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to existing application files or create new integration examples based on the user's package manager, environment variable, AI SDK function, provider, and selected You.com tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
