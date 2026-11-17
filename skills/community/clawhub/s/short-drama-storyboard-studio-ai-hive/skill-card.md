## Description:

Creates Chinese short-drama storyboard workflows, shot lists, prompt plans, runnable AI-HIVE commands, and continuity checks from scripts, character or scene boards, style, aspect ratio, and runtime inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, directors, writers, comic-drama teams, and AI video creators use this skill to turn short-drama, commerce, advertising, and social-media concepts into storyboard-ready scripts, shot tables, generation prompts, task records, and acceptance checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials could be sent to an untrusted custom endpoint if AI_HIVE_BASE_URL or --base-url is set from untrusted instructions.

Mitigation: Use only the default AI-HIVE endpoint unless the custom deployment is fully trusted, and review endpoint settings before running generation commands.

Risk: Generation tasks can upload or download media and may incur costs.

Mitigation: Confirm prompts, media inputs, routing mode, batch size, and model parameters before submitting generation jobs; start with a small sample for batch work.

Risk: Storyboard or marketing outputs may misuse copyrighted references, unsupported product claims, or fake endorsements.

Mitigation: Require authorized source materials and verified factual claims, and use only abstract structural analysis when rights or evidence are unclear.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/short-drama-storyboard-studio-ai-hive)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON task records, and optional generated media file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE model routing choices, price snapshots, task IDs, upload/download records, and ffmpeg processing commands after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
