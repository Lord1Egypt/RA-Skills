## Description:

TSW Shorts Factory helps agents set up a quote-based YouTube Shorts pipeline using local text-to-speech audio, Pexels stock clips, MoviePy assembly, and YouTube draft or unlisted upload flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vanyanski](https://clawhub.ai/user/vanyanski)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to configure an automated pipeline that turns quote libraries into vertical YouTube Shorts drafts for human review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates YouTube uploads and uses persistent OAuth access.

Mitigation: Run it only with a contained YouTube account, keep uploads as drafts or unlisted until manually reviewed, and audit the uploader path before production use.

Risk: The security review warns not to rely on the draft or unlisted upload claim unless the missing uploader script is supplied and audited.

Mitigation: Require the uploader implementation during review and verify the final YouTube privacy status before enabling scheduled runs.

Risk: The security guidance flags an exposed Pexels key, pickle token storage, hard-coded root paths, external sys.path injection, and unpinned dependencies.

Mitigation: Rotate the exposed key, move secrets to environment-managed credentials, replace pickle token storage, remove hard-coded paths and sys.path injection, and pin dependencies before production deployment.

## Reference(s):

- [YouTube OAuth Setup](references/youtube-setup.md)
- [Google Cloud Console](https://console.cloud.google.com/)
- [TSW Shorts Factory on ClawHub](https://clawhub.ai/vanyanski/skills/tsw-shorts-factory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON examples, and Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent guidance can lead to local MP4 files, cached media, audio files, OAuth token files, and YouTube upload attempts when the bundled scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
