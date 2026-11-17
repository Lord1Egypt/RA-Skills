## Description:

Creates Chinese short-drama trailer remake workflows, including structure analysis, suspense beats, character conflicts, subtitle cards, original adaptation plans, shot lists, AI-HIVE generation commands, and continuity checks for authorized materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, short-drama promotion teams, paid acquisition teams, and editors use this skill to turn authorized reference trailers and source footage into reviewable Chinese production plans, prompts, runnable AI-HIVE commands, and acceptance checklists. It is intended for original adaptation of emotional pacing and information rhythm, not copying protected footage, dialogue, music, logos, or creator identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE API credentials can be sent to a custom base URL if a user supplies --base-url, AI_HIVE_BASE_URL, or a stored base_url.

Mitigation: Use the default AI-HIVE endpoint unless the endpoint is fully trusted, and review configuration before running commands that use an API key.

Risk: Image and video generation commands can submit potentially billable jobs and batch requests.

Mitigation: Confirm prompts, model or routing mode, pricing snapshot, and batch size before submitting generation tasks; start with a small sample when uncertain.

Risk: Uploaded reference media may include copyrighted, branded, private, or otherwise unauthorized content.

Mitigation: Only upload media the user is authorized to use, and restrict unauthenticated references to abstract structure analysis and original creative alternatives.

Risk: Trailer remake workflows can drift into copying protected dialogue, shots, music, logos, or creator identity.

Mitigation: Keep reuse at the level of emotional curve, information order, shot function, and rhythm; rewrite characters, scenes, dialogue, visual style, and branding.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/short-drama-trailer-remake-ai-hive)
- [AI-HIVE Chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API Base](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown with script, prompt, command, task-record, and checklist sections; helper scripts can produce JSON briefs and downloaded media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE routing choices, pricing snapshots, task IDs, status records, file locations, and ffmpeg processing commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
