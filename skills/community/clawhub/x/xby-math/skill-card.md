## Description:

一个高性能的数学计算协议服务器，提供从基础算术到高级微积分和线性代数的全面数学计算功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to route math requests to calculation tools for arithmetic, percentages, arrays, statistics, financial calculations, matrix operations, calculus, and multi-step computation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calculation inputs and the API key are sent to a third-party XiaoBenYang service.

Mitigation: Install only if you trust the service, verify the configured endpoint, and avoid submitting sensitive financial or private datasets.

Risk: The required API key may be stored in a local plaintext .env file.

Mitigation: Use a narrowly scoped, revocable key and remove any .env-stored key when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/xby-math)
- [Publisher profile](https://clawhub.ai/user/cainingnk)
- [XiaoBenYang API key service](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries of JSON API results with optional inline code or configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key and sends calculation inputs to a third-party API.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
