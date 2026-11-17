## Description:

Turns Xiaohongshu viral-video teardown requests into an executable Chinese content workflow, runnable AI-HIVE commands, and deliverables such as teardown reports, scripts, prompts, shot lists, and acceptance checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External Xiaohongshu brands, creators, and content marketing teams use this skill to turn authorized reference videos, product facts, audience details, scenarios, and account voice into original content plans, scripts, prompts, and review checklists. Developers and operators can also use the bundled scripts to create production briefs, submit AI-HIVE generation jobs, and perform deterministic video checks or edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and selected media may be sent to a configured AI-HIVE server.

Mitigation: Use the default AI-HIVE endpoint, avoid custom base URLs unless explicitly trusted, and use a restricted or disposable API key.

Risk: Image or video generation can create billable tasks.

Mitigation: Confirm the final prompt, mode, routing preference, and generation parameters before submitting tasks, and start with a small sample for batch work.

Risk: Reference-video teardown can drift into unauthorized copying, unsupported product claims, or misleading user testimony.

Mitigation: Use only authorized materials, preserve factual product claims, and transform the reference into a distinct script, scene design, voice, and visual style.

Risk: Local helper scripts depend on Python packages and ffmpeg.

Mitigation: Install dependencies in a virtual environment and run deterministic video edits on copies while preserving the original media.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/xiaohongshu-viral-video-decomposer-ai-hive)
- [AI-HIVE entry point](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, JSON file outputs, and downloadable media paths when generation jobs are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks for confirmation before billable generation tasks and records routing, model, price snapshot, taskId, status, and file locations when applicable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
