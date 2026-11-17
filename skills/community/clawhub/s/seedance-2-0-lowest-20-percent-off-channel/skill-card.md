## Description:

Helps creators, marketing teams, ecommerce teams, and short-form video teams generate Seedance 2.0 videos through AI Hive from text prompts and optional image, video, or audio references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, ecommerce operators, and content production teams use this skill to submit Seedance 2.0 video generation jobs through AI Hive, upload reference media when needed, track task status, and download generated videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and supplied image, video, or audio media are uploaded to AI Hive for generation.

Mitigation: Use only content you are authorized to upload, and avoid sensitive or confidential media unless AI Hive handling terms are acceptable for the use case.

Risk: The API destination can be changed with --base-url, AI_HIVE_BASE_URL, or config base_url.

Mitigation: Use the default AI Hive endpoint or another explicitly trusted endpoint; do not run the skill with an untrusted base URL.

Risk: Video generation can incur charges, and discount or pricing claims depend on the runtime pricing snapshot.

Mitigation: Review the current pricing snapshot before submitting jobs, confirm batch or repeated runs before high-volume use, and verify promotional pricing independently.

Risk: Running init stores an API key locally.

Mitigation: Keep ~/.ai-hive/config.json restricted to the user, prefer environment variables or command-line injection on shared systems, and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-2-0-lowest-20-percent-off-channel)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, task status JSON, and downloaded video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store an AI Hive API key in ~/.ai-hive/config.json and may download generated media to ~/Downloads/AiHive or a user-selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG.md top entry lists 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
