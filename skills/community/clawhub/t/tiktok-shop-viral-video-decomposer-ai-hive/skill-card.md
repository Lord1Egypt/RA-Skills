## Description:

Helps cross-border sellers, TikTok Shop teams, and content operators turn authorized reference videos and product facts into localized commerce video breakdowns, UGC scripts, prompts, review checklists, and optional AI-HIVE generation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketers, and content operators use this skill to analyze TikTok Shop-style short-form commerce videos, create differentiated scripts and prompts, and prepare AI-HIVE video generation or editing commands while preserving authorization and factual-review checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a paid AI-HIVE API credential.

Mitigation: Use environment or local config storage instead of command-line keys when shell history or process listings matter, and avoid exposing keys in files, logs, screenshots, or version control.

Risk: The API endpoint can be configured, which can route credentials or media to an unintended host.

Mitigation: Before use, confirm the configured base URL is the official AI-HIVE HTTPS endpoint shown in the evidence.

Risk: The workflow can upload proprietary reference images, video, or audio.

Mitigation: Upload only explicitly selected media that the user is authorized to provide to AI-HIVE.

Risk: Generation calls may be billable and may submit parameters the user has not reviewed.

Mitigation: Review prompts, model choice, routing mode, pricing snapshot, and batch parameters before submission; use a small sample before batch work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/tiktok-shop-viral-video-decomposer-ai-hive)
- [AI-HIVE Chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI Base](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline JSON and bash/Python command examples; bundled scripts can emit JSON briefs, task records, generated media files, and downloaded outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call AI-HIVE APIs, upload explicitly selected media files, poll asynchronous jobs, and write outputs to user-selected paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
