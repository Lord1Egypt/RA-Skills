## Description:

Fetches the real-time Weibo hot-search ranking from TianAPI and returns trending terms, heat scores, labels, and topic links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer requests about current Weibo trending topics by calling the TianAPI Weibo Hot API with a configured API key and presenting the results as a readable list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a TianAPI key, and passing API keys on the command line or in query strings can expose secrets through shell history, process listings, or logs.

Mitigation: Prefer TIANAPI_WEIBO_HOT_KEY in the environment, avoid command-line keys, and do not commit scripts/.env.

Risk: The bundled helper script appears broken as written, including an intended JSON mode and method call mismatch.

Mitigation: Fix and test the script before relying on it in an agent workflow, especially argparse handling for JSON output and the TianAPI fetch method name.

Risk: TianAPI quota, API approval, invalid keys, or network timeout can prevent successful retrieval.

Mitigation: Handle TianAPI error codes clearly, retry network timeouts once, and tell the user when quota, approval, or credential action is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/workxin/skills/tianapi-weibo-hot)
- [TianAPI Weibo Hot API documentation](https://www.tianapi.com/apiview/100)
- [TianAPI Weibo Hot API endpoint](https://apis.tianapi.com/weibohot/index)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Readable topic lists with hot-search labels, heat scores, and links; setup and usage guidance may include inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and TIANAPI_WEIBO_HOT_KEY; no third-party Python package dependencies are declared.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
