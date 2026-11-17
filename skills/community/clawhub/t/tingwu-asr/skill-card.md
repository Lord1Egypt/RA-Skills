## Description:

Uses Alibaba Cloud Tingwu to transcribe local or linked audio and video into Markdown transcripts, with support for speaker separation, batch processing, archives, and optional video slide extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agent operators use this skill to submit audio or video to Alibaba Tingwu for cloud transcription, then receive Markdown transcript files suitable for review, archiving, or downstream summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to an Alibaba/Tingwu account and uploads selected audio or video to Alibaba Cloud.

Mitigation: Use a dedicated account where possible and avoid sensitive or regulated recordings unless cloud processing is acceptable.

Risk: The skill handles account passwords and reusable session cookies.

Mitigation: Do not place real cookies in command-line arguments or chats; protect config/.env and config/cookies.json with strict local permissions and rotate credentials if they are exposed.

Risk: The workflow depends on reverse-engineered Tingwu web APIs and browser login behavior that may change.

Mitigation: Review before deployment and test authentication plus a small transcription job before relying on the skill for important recordings.

## Reference(s):

- [Tingwu ASR ClawHub page](https://clawhub.ai/cat-xierluo/skills/tingwu-asr)
- [Publisher profile](https://clawhub.ai/user/cat-xierluo)
- [Project homepage](https://github.com/cat-xierluo/legal-skills)
- [Tingwu internal REST API reference](references/api-capture.md)
- [Alibaba Tingwu web app](https://tingwu.aliyun.com/home)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown transcript files, status text, archive files, JSON task state, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create source-adjacent transcript files, archive directories, pending/completed task JSON, cookie state, quota history, and video slide image folders.]

## Skill Version(s):

0.4.2 (source: frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
