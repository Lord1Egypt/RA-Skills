## Description:

This skill helps brands, merchants, and creative teams turn visual ASMR loop-ad ideas into production briefs, storyboard prompts, AI-HIVE video-generation commands, delivery records, and seamless-loop checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketing teams, and commerce operators use this skill to plan and generate short-form visual loop advertisements with clear product anchors, platform constraints, and review checklists. It supports blueprint creation, prompt drafting, AI-HIVE task submission, media upload, polling, download, and deterministic video edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured API key can be sent to a configurable AI-HIVE-compatible endpoint.

Mitigation: Use the default AI-HIVE endpoint unless the publisher and endpoint are trusted, and review AI_HIVE_BASE_URL, --base-url, and ~/.ai-hive/config.json before authenticated use.

Risk: Generation commands may upload user media and incur charges.

Mitigation: Confirm the prompt, model, routing mode, pricing snapshot, and uploaded media before running generation or batch commands.

Risk: Broad invocation can produce advertising guidance that overstates product claims, platform performance, or authorization status.

Mitigation: Require source-backed product facts, authorized assets, and human review for claims, platform compliance, trademarks, privacy, and likeness rights.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/satisfying-loop-ad-ai-hive)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON records and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON briefs and downloaded image or video files when the user runs the provided commands with valid AI-HIVE credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
