## Description:

Tieba Spider crawls Baidu Tieba threads, including post content, images, and sub-post replies, and exports the result as Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuxiaoji](https://clawhub.ai/user/fuxiaoji)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to archive Baidu Tieba threads as local Markdown, with optional local image downloads and sub-post capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler contacts Tieba over network APIs and may download files from thread content.

Mitigation: Use it only where that network activity is acceptable, prefer --no-images on untrusted networks or untrusted threads, and review generated files before sharing them.

Risk: Output is written to local directories selected by the user.

Mitigation: Choose a dedicated output directory and inspect the generated Markdown and image files before reusing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fuxiaoji/skills/tieba-spider)
- [Publisher profile](https://clawhub.ai/user/fuxiaoji)
- [Baidu Tieba thread URL format](https://tieba.baidu.com/p/7487460366)
- [Baidu Tieba mobile API endpoint used by artifact](http://c.tieba.baidu.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown files and local image files with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a per-thread output directory containing a Markdown export and, unless disabled, downloaded image files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
