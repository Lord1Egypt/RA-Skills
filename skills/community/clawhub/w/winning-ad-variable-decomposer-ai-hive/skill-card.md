## Description:

Helps ad buyers, directors, agencies, and growth teams decompose authorized winning ads into transferable hooks, roles, scenes, proof points, pacing, CTA variables, scripts, prompts, and AI-HIVE generation workflows without copying protected expression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing, ecommerce, advertising, short-video, and social growth teams use this skill to turn authorized reference ads and product facts into reviewable decomposition reports, differentiated remake plans, shot scripts, generation prompts, command examples, and acceptance checklists. It is also useful for agents that need to create AI-HIVE video-generation tasks after human confirmation of budget, routing, and source-material rights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A stored bearer API key can be sent to a custom AI-HIVE base URL if the endpoint is changed.

Mitigation: Use the default AI-HIVE endpoint unless the custom endpoint is fully trusted; keep API keys scoped, revocable, and out of logs, screenshots, and repositories.

Risk: Generated media downloads may write files into an output directory selected by the user and informed by task results.

Mitigation: Run downloads in a low-risk output directory and review downloaded filenames and locations before using them in downstream workflows.

Risk: The workflow could be misused for unauthorized ad copying, unsupported product claims, or fabricated testimonials.

Mitigation: Require authorized source material, keep copied content at the level of transferable structure, mark unverified facts for review, and avoid claims that lack product or platform evidence.

Risk: Image or video generation may incur cost.

Mitigation: Confirm final prompts, model, routing mode, and budget before submitting billable generation tasks; start with a small sample for batch work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/winning-ad-variable-decomposer-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional JSON files and inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task records such as model, routing mode, price snapshot, taskId, status, and downloaded file locations when generation is performed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
