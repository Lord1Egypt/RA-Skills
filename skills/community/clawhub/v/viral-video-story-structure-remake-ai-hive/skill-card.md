## Description:

This skill helps brand content teams, short-drama writers, and advertising creatives turn authorized viral-video references into original story beats, escalation structure, reversal points, brand-integration moments, storyboards, prompts, runnable AI-HIVE commands, and review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand content teams, short-drama writers, advertising creatives, and developers use this skill to analyze authorized reference material and produce original commercial short-video plans, scripts, prompts, task records, shell commands, and quality checks. It is intended for workflows that preserve structural inspiration while avoiding copied characters, dialogue, shots, protected expression, false product claims, and platform-rule evasion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE API credentials may be sent to an arbitrary configured endpoint if --base-url, AI_HIVE_BASE_URL, or ~/.ai-hive/config.json is changed.

Mitigation: Use the default AI-HIVE endpoint unless the endpoint is explicitly trusted, avoid passing credentials to untrusted URLs, and review ~/.ai-hive/config.json before running credentialed commands.

Risk: Media uploads, downloads, and asynchronous generation jobs can process local files and may incur costs.

Mitigation: Confirm prompts, files, routing mode, model choice, and budget before generation; use small samples first and keep task records for submitted jobs.

Risk: Story-structure remake workflows can create copyright, likeness, endorsement, or misleading product-claim issues if reference material and brand facts are not authorized and verified.

Mitigation: Use only authorized reference assets, keep characters, dialogue, shots, music, logos, and protected expression distinct, and require human review for brand claims and regulated content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/viral-video-story-structure-remake-ai-hive)
- [AI-HIVE web application](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured sections, inline shell commands, JSON task records, generated script or prompt text, and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON briefs, process local media with ffmpeg, upload reference media, submit asynchronous AI-HIVE generation jobs, poll task status, and download generated media after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
