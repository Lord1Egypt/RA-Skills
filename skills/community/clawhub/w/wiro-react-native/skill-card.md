## Description:

Use the official @wiro-ai/wiro-react-native SDK to run Wiro models from React Native and Expo apps, including typed and catalog requests, file uploads, task tracking, cancellation, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiroai](https://clawhub.ai/user/wiroai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate Wiro model generation into React Native and Expo apps, including sending requests, uploading files, tracking tasks, and handling results and errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install instructions do not pin an SDK version, so installation may resolve to a different release over time.

Mitigation: Review the package and selected version before installing, and use the project's dependency lockfile.

Risk: A configured proxy endpoint receives app requests and may handle prompts or uploaded media.

Mitigation: Use a trusted HTTPS endpoint and review how your backend handles credentials and submitted content.

## Reference(s):

- [Wiro API documentation](https://wiro.ai/docs/introduction)
- [Wiro model catalog](https://wiro.ai/models)
- [Wiro pricing](https://wiro.ai/product/pricing)
- [React Native SDK source](https://github.com/wiroai/ReactNative-QuickStart)
- [React Native SDK package](https://www.npmjs.com/package/@wiro-ai/wiro-react-native)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with TypeScript and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
