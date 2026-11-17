## Description:

vidunderstand converts a local video file or public video URL into a cleaned transcript and can use a prompt to produce summaries, social media copy, meeting notes, quote lists, scripts, or translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users and content teams use this command skill to transcribe spoken video or audio and transform the transcript into summaries, captions, marketing copy, meeting minutes, scripts, or translations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL inputs can fetch arbitrary network resources and upload selected videos, video URLs, prompts, task IDs, and filename metadata to the GuaiKei cloud service and upload storage.

Mitigation: Use only with public or approved media, avoid confidential meetings, customer data, private intranet URLs, localhost URLs, cloud metadata URLs, and sensitive recordings unless the provider's data handling and network controls have been verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/vidunderstand)
- [GuaiKei service website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown, depending on the user prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The command writes the final transcript or generated copy to stdout; progress and diagnostics are written to stderr.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
