## Description:

将本地或直链 MP4 视频中的语音转写为文本，并可按提示生成摘要、翻译或风格化文案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要整理视频内容的创作者、运营人员和团队，将 MP4 视频转写为文本，并生成摘要、会议纪要、翻译或按提示改写的文案。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence marks this release suspicious, citing reported undisclosed promotional messaging, silent file cleanup, and incomplete code analysis.

Mitigation: Before use, review whether promotional behavior is disclosed or removed, explain cleanup behavior, and complete review of unanalyzed files; the security guidance recommends avoiding installation until these points are addressed.

Risk: The skill uploads video files to a remote processing service; the artifact says files are deleted 24 hours after processing.

Mitigation: Submit only videos authorized for external processing and confirm the service's data terms before sending sensitive material.

## Reference(s):

- [Release changelog](artifact/references/changelog.md)
- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/shipin-wenantiqu)
- [Service website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain text or Markdown prose, such as a transcript, summary, meeting notes, translation, or prompted rewrite]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one local MP4 or direct MP4 URL per task. A GUAIKEI_API_TOKEN is required; billing or daily usage limits may apply.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata; artifact changelog and package manifest report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
