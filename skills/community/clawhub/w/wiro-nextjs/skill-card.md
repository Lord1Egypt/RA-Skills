## Description:

Build Next.js App Router features on Wiro AI by keeping API keys in server routes and actions, discovering models and showing prices, starting and tracking tasks, uploading inputs, and streaming chat through the Wiro LLM gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiroai](https://clawhub.ai/user/wiroai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building Next.js App Router applications use this skill to integrate Wiro model APIs through server routes and actions, including model discovery, price display, task tracking, file uploads, and streaming chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was benign but had medium confidence, covered 83.3% of components, and leaves some uncertainty.

Mitigation: Review the skill and confirm that its network and environment access fit the application before installing.

Risk: The examples send prompts and uploaded files to Wiro APIs, and model runs may incur charges.

Mitigation: Review the data sent to Wiro, keep API credentials in server-side environment variables, and set run limits or team spend limits.

Risk: A public deployment can expose paid runs, and the example webhook notifications are unsigned.

Mitigation: Restrict access and run prices, then verify webhook task IDs with Wiro before acting on a notification.

## Reference(s):

- [Wiro Run API](https://wiro.ai/docs/run-a-model)
- [Wiro Tasks](https://wiro.ai/docs/tasks)
- [Wiro Model Parameters and Webhooks](https://wiro.ai/docs/model-parameters)
- [Wiro Authentication](https://wiro.ai/docs/authentication)
- [Wiro LLM Gateway](https://wiro.ai/docs/completions-api)
- [Wiro Models Catalog](https://wiro.ai/models)
- [Wiro Next Starter](https://github.com/wiroai/Wiro-Next-Starter)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Guidance]

**Output Format:** [TypeScript and TSX examples with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Next.js App Router route handlers, server actions, shared server helpers, and a client chat component.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
