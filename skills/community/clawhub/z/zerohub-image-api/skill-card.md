## Description:

zeroHub Image API helps agents use a user-provided ZEROHUB_API_KEY to check balance, submit image generation jobs, poll results, and optionally download generated images to a user-selected directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenzihao0731](https://clawhub.ai/user/chenzihao0731)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect an agent workflow to zeroHub image generation, including balance checks, task submission, polling, and controlled local downloads of generated files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a billing credential for zeroHub image generation.

Mitigation: Treat ZEROHUB_API_KEY as a billing credential, keep command tracing disabled, and confirm image-generation requests before execution.

Risk: Changing ZEROHUB_BASE_URL, --allowed-host, or --allow-http can relax the default network and download protections.

Mitigation: Use the default zeroHub endpoint and HTTPS-only host policy unless the alternate host or download URL is fully trusted.

Risk: Downloaded image files are written to a user-selected directory.

Mitigation: Choose an output directory private to the current user and review downloaded files before sharing them onward.

## Reference(s):

- [zeroHub website](https://zerohub.zhyy.ltd)
- [zeroHub API documentation](https://zerohub.zhyy.ltd/docs)
- [ClawHub skill page](https://clawhub.ai/chenzihao0731/skills/zerohub-image-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and structured JSON from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local image files when downloads are requested.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
