## Description:

This skill helps short-drama, art, comics, and AI video production teams turn scripts, character relationships, settings, visual styles, and references into character bibles, stable appearance anchors, costume changes, expression and action libraries, protected attributes, reference-image tasks, and AI-HIVE media-generation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creative, marketing, ecommerce, short-drama, comics, and AI video teams use this skill to plan character-consistent Chinese short-form story workflows and produce reviewable briefs, shot tasks, prompts, code commands, and continuity checklists before any paid media generation is submitted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE API keys may be sent to a configurable endpoint.

Mitigation: Use the default AI-HIVE endpoint or another endpoint only after trust review, keep API keys scoped and revocable, and avoid placing secrets in files, logs, screenshots, or version control.

Risk: Media workflows may rely on remote upload, polling, and download URLs.

Mitigation: Review generated commands and downloaded files, use authorized input media only, and run helper scripts in a controlled virtual environment with pinned dependencies where possible.

Risk: Image or video generation can incur cost or produce misleading commercial claims.

Mitigation: Confirm prompts, routing mode, model choice, pricing snapshot, and factual claims before submitting paid generation tasks.

## Reference(s):

- [AI-HIVE entry point](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI base endpoint](https://ai-hive.iclip.cn/api)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/short-drama-character-bible-ai-hive)
- [Publisher profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with runnable shell commands and optional JSON, image, video, and edited media files from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks for human confirmation before potentially billable AI-HIVE image or video generation and records routing, model, pricing snapshot, taskId, status, and downloaded file locations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
