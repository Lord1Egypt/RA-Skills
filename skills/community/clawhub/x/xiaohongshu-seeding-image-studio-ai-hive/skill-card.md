## Description:

Turns Xiaohongshu seeding-image requests into reviewable visual blueprints, image prompts, reference-image strategies, batch variants, delivery checklists, and optional AI-HIVE image-generation commands for commercial content teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brands, creators, seeding teams, lifestyle merchants, and their supporting developers use this skill to plan and produce Xiaohongshu-ready covers, process images, detail images, comparison images, and post image sets from authorized product facts and reference materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if provided on the command line or sent to an untrusted custom API host.

Mitigation: Use the default HTTPS AI-HIVE endpoint, prefer environment or local config storage for the API key, and avoid --api-key in shell history or logs.

Risk: Reference media and prompts may be uploaded for billable generation.

Mitigation: Confirm authorization, route, model, price snapshot, and small-batch parameters before submitting generation jobs.

Risk: Generated seeding content can mislead users if it invents product claims, endorsements, or results.

Mitigation: Use only confirmed product facts and authorized assets, and review outputs for false testimonials, unsupported efficacy claims, and platform-rule issues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/xiaohongshu-seeding-image-studio-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands and optional JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON and downloaded generated media after user confirmation and authenticated AI-HIVE API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
