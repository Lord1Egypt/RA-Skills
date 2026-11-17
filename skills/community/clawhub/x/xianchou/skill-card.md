## Description:

Xianchou CLI guides agents to generate images and videos through Xianchou's CLI API and to insert generated images into Markdown or MDX documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[starlying](https://clawhub.ai/user/starlying)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content authors, and external agents use this skill to configure and operate the Xianchou CLI for AI image generation, AI video generation, file upload, task polling, and Markdown or MDX image insertion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a globally installed, unpinned @xianchou/cli package that handles credentials and local files.

Mitigation: Install only a trusted reviewed CLI version, prefer pinning the package version, and avoid running the CLI with elevated privileges.

Risk: Xianchou access keys and project IDs are used for remote generation and upload workflows.

Mitigation: Use a limited project access key, store credentials only in the documented config path or environment variables, and rotate credentials if exposure is suspected.

Risk: Local image, video, or audio files may be uploaded and returned as publicly accessible URLs.

Mitigation: Avoid uploading sensitive local media and review file paths before invoking generate or upload commands.

Risk: Markdown or MDX content can be modified when the --write flag is used.

Mitigation: Review dry-run output first and use version control or backups before writing generated image references into source documents.

## Reference(s):

- [Xianchou CLI skill page](https://clawhub.ai/starlying/skills/xianchou)
- [Xianchou homepage](https://xianchou.com)
- [Xianchou CLI npm package](https://www.npmjs.com/package/@xianchou/cli)
- [CLI command guide](references/cli-command-guide.md)
- [API generation guide](references/api-generation-guide.md)
- [Markdown image guide](references/markdown-image-guide.md)
- [API contract guide](references/api-contract-guide.md)
- [Common pitfalls](references/common-pitfalls.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate and upload media assets, poll remote tasks, and write changes to Markdown or MDX files only when the --write flag is used.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
