## Description:

This skill helps WeChat Channels operators, brand content teams, and commerce sellers decompose authorized viral short-video references into hooks, shot structure, rewritten scripts, prompts, runnable AI-HIVE commands, and review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video operators, brand content teams, and developers use this skill to turn an authorized reference video, product facts, audience, and account positioning into an original short-video production workflow for commerce, advertising, marketing, and social publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AI-HIVE API key and can read credentials from command-line input, environment variables, or ~/.ai-hive/config.json.

Mitigation: Use a scoped API key, do not paste real keys into prompts or logs, review the configured environment and config file before running commands, and rotate the key if it is exposed.

Risk: The workflow can upload selected local media and download generated results through AI-HIVE network endpoints.

Mitigation: Upload only authorized media, avoid custom base URLs unless they are fully controlled, and use --no-download for dry runs or when reviewing task parameters before transfer.

Risk: Video generation may create paid tasks after model, routing, and pricing parameters are selected.

Mitigation: Confirm the final prompt, model, routing mode, parameters, and price snapshot before execution, and test with a small sample before batch generation.

Risk: The skill is designed for viral-video decomposition and could be misused for unauthorized copying, false product claims, fabricated testimonials, or platform-rule evasion.

Mitigation: Use only authorized references, keep scripts and visuals materially different from protected source content, require factual support for product claims, and run human review before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/shipinhao-viral-video-decomposer-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, optional JSON files, and downloaded media files from AI-HIVE tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE task IDs, routing mode, model identifiers, price snapshots, status details, file locations, and acceptance checklist results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
