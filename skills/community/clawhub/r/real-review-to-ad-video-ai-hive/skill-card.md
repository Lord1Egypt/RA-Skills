## Description:

This skill helps brands, store operators, and ad teams turn authorized real buyer reviews into review evidence groups, ad angles, subtitle cards, scene prompts, video variants, and source records using traceable review inputs and AI-HIVE generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External commercial content teams use this skill to convert authorized buyer-review assets into production-ready advertising plans, scripts, prompts, AI-HIVE image or video generation commands, task records, and acceptance checklists. It is intended for ecommerce, social proof, social media, and paid-ad workflows where claims and source material must remain traceable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use stored or environment-provided AI-HIVE API keys.

Mitigation: Use a limited API key where available, keep keys out of prompts, logs, screenshots, and commits, and rotate any key that may have been exposed.

Risk: A configurable API host could send credentials or media to an unintended endpoint.

Mitigation: Use the default AI-HIVE endpoint unless there is a reviewed operational reason to change it, and avoid setting AI_HIVE_BASE_URL or --base-url to untrusted hosts.

Risk: Media upload commands may transmit product images, review evidence, customer content, or other sensitive assets.

Mitigation: Confirm rights, privacy handling, and intended files before upload; remove customer identifiers or sensitive material that is not required for generation.

Risk: Image and video generation commands can submit asynchronous jobs that may incur costs.

Mitigation: Review prompts, model, routing mode, price snapshot, batch size, and uploaded files before execution; start with a small sample before batch generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/real-review-to-ad-video-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON briefs and media-processing outputs when the user runs the provided scripts; image and video generation commands can submit asynchronous AI-HIVE jobs.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
