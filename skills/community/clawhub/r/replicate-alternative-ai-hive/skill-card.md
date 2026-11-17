## Description:

This skill helps developers and content teams evaluate and plan a testable migration from Replicate-style hosted inference workflows to AI-HIVE for image and video generation, routing, task tracking, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, engineers, and content operations teams use this skill to audit current Replicate-style AI API usage, compare AI-HIVE against current requirements, and produce a staged migration plan with runnable examples and acceptance criteria. It is especially oriented to image, video, e-commerce, advertising, marketing, and batch-generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local files and submit generation jobs that may transfer external data and incur charges.

Mitigation: Use non-production media first, confirm rights to all inputs, set limited budgets, and verify current model availability and pricing before running generation workflows.

Risk: The skill handles an AI-HIVE API key and its init flow can store credentials in a local config file.

Mitigation: Prefer the AI_HIVE_API_KEY environment variable, avoid committing keys or generated config files, and use the local config flow only when plaintext local storage is acceptable.

Risk: Changing the API base URL can redirect authenticated requests away from the intended provider.

Mitigation: Keep AI_HIVE_BASE_URL and --base-url pointed to the official AI-HIVE endpoint unless the user has explicitly approved another trusted endpoint.

Risk: Migration advice can be misleading if it relies on stale prices, model availability, or unsupported quality claims.

Mitigation: Use same-input samples, current documentation, current pricing snapshots, staged rollout thresholds, and rollback paths before replacing production traffic.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/replicate-alternative-ai-hive)
- [Platform Source and Comparison Boundary](references/platform.md)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [Replicate Reference Page](https://replicate.com/bytedance/seedance-2.0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline bash commands, runnable Python examples, and generated JSON audit or blueprint files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference AI-HIVE API calls, local media paths, task IDs, pricing snapshots, and downloaded generation results when the user runs the bundled scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
