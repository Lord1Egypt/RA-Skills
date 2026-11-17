## Description:

Helps creators and commercial content teams turn authorized reference-motion video requests into Chinese production plans, prompts, AI-HIVE generation commands, task records, and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to plan and run authorized reference-motion short-video workflows for ecommerce, advertising, social media, virtual IP, dance, sport, and product-showcase content. It helps produce reviewable briefs, storyboards, prompts, AI-HIVE API commands, task tracking details, and acceptance checks before billable generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API bearer key can be sent to an arbitrary configured base URL if AI_HIVE_BASE_URL or the local AI-HIVE config is changed.

Mitigation: Use the default AI-HIVE API endpoint unless the custom endpoint is fully trusted, and review AI_HIVE_BASE_URL plus ~/.ai-hive/config.json before running commands with an API key.

Risk: Generation can be billable and may upload user-provided media.

Mitigation: Confirm prompts, route, model parameters, media authorization, and upload intent before submitting generation tasks; start with a small sample for batch work.

Risk: Reference-motion workflows can be misused for unauthorized likeness, choreography, copyrighted content, false product claims, or fake endorsements.

Mitigation: Require authorization for reference media and protected identities, keep factual claims marked for verification, and produce abstract structure guidance instead of replication when rights are unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/reference-motion-transfer-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline bash commands and JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create blueprint JSON files, submit AI-HIVE generation tasks, upload authorized media, poll asynchronous task status, and download generated image or video files when the user confirms billable operations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
