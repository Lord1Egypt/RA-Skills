## Description:

YouTube long video transcription and translation workflow for extracting English subtitles, translating them to Chinese, and producing formatted transcript documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingliu1617-art](https://clawhub.ai/user/qingliu1617-art)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to process long YouTube videos, retrieve English subtitle tracks through DownSub, translate transcripts to Chinese, and deliver the result as a Markdown document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published skill embeds a concrete bearer credential.

Mitigation: Revoke or rotate the published credential and require users to provide their own secret from a safe configuration source before use.

Risk: Using the workflow sends YouTube URLs and transcript requests to DownSub and may upload generated Markdown through zhiyan.

Mitigation: Confirm data-sharing requirements before use and disable optional upload unless the destination is approved.

Risk: Incorrect subtitle language selection can produce inaccurate or nonsensical translation output.

Mitigation: Check the DownSub response language field and proceed only with English tracks marked en or en-auto.

Risk: The workflow creates local transcript files that may contain sensitive or copyrighted content.

Mitigation: Store generated files in an approved location and review content before sharing or uploading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qingliu1617-art/skills/ytb-transcript-long)
- [DownSub transcript download API endpoint](https://api.downsub.com/download)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown transcript documents with Chinese translation, executive summary, and metrics table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local transcript files and optionally upload generated Markdown through zhiyan when available.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
