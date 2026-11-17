## Description:

Use UniFuncs Deep Search API for fast, comprehensive information gathering when users ask for deep search, broad investigation, or in-depth topic coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinlic](https://clawhub.ai/user/vinlic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run UniFuncs Deep Search for multi-step information gathering, consolidated research reports, and asynchronous deep-search task workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deep-search queries, prompts, and related task content are sent to UniFuncs using the user's API key.

Mitigation: Use the skill only for content appropriate to share with UniFuncs and avoid including secrets or sensitive internal information in queries.

Risk: The --push-to-share and --set-public options can share or publish results when intentionally enabled.

Mitigation: Leave sharing options disabled unless public or shared result visibility is expected for the task.

Risk: Report mode may continue receiving streamed output in a background process after the visible command returns.

Mitigation: Use explicit timeouts, read the named stream file when needed, and avoid placing custom stream files in shared directories.

## Reference(s):

- [UniFuncs account and API key setup](https://unifuncs.com/account)
- [UniFuncs Deep Search ClawHub listing](https://clawhub.ai/vinlic/skills/unifuncs-deep-search)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or plain text reports, task IDs, and optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stream partial report content to a local stream file and later render accumulated results.]

## Skill Version(s):

0.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
