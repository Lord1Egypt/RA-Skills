## Description:

Generate video and images by calling the official Vidu API via vidu CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvinzhao](https://clawhub.ai/user/calvinzhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate or edit Vidu images, videos, speech, lip-sync outputs, and video compositions from prompts and local media. It also guides task submission, polling, cost checks, quota checks, reference element management, and result download workflows through vidu-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact installs a mutable external vidu-cli package that downloads a platform binary.

Mitigation: Review before installing and prefer a pinned, verified vidu-cli release instead of installing a mutable latest package globally.

Risk: Prompts, images, video, audio, and task settings are sent to Vidu's API for processing.

Mitigation: Avoid sensitive or regulated media and prompts unless that processing is approved for the deployment context.

Risk: A Vidu API token is required for operation.

Mitigation: Use a least-privilege Vidu token and keep VIDU_TOKEN out of shared logs, examples, and committed configuration.

Risk: Debug mode can print full API response bodies to stderr.

Mitigation: Keep VIDU_DEBUG disabled in shared terminals, logs, and support bundles unless the output has been reviewed.

## Reference(s):

- [Vidu Homepage](https://www.vidu.cn/)
- [vidu-cli npm package](https://www.npmjs.com/package/vidu-cli)
- [Vidu Task Parameters Reference](references/parameters.md)
- [Video Compose Reference](references/compose.md)
- [Errors and Retry Strategy](references/errors_and_retry.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON, Files]

**Output Format:** [Markdown guidance with shell commands and JSON CLI response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce task IDs, trace IDs, error fields, and downloaded media file paths from vidu-cli workflows.]

## Skill Version(s):

1.4.9 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
