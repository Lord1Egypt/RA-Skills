## Description:

Use Vidau Open API to generate short videos with Veo3, Sora2, and other models, or query account credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigjoehuang](https://clawhub.ai/user/bigjoehuang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create short videos through the Vidau Open API, upload local media as generation inputs, query model capabilities, check task status, and inspect account credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports requests for privileged system changes during environment setup.

Mitigation: Use the skill only in environments where Python is already installed, and do not allow sudo or package-manager installation commands during skill execution.

Risk: The security evidence reports that the skill can upload broad local files to Vidau.

Mitigation: Upload only non-sensitive media files that the user intentionally wants to send to Vidau.

Risk: The security evidence reports persistent local logs and caches for API activity.

Mitigation: Protect or periodically delete Vidau log and cache files, and set cache or log paths to controlled locations when needed.

## Reference(s):

- [Vidau API Introduction](https://doc.superaiglobal.com/en/overview/introduction)
- [Vidau Website](https://vidau.ai)
- [Vidau Model Overview](https://doc.superaiglobal.com/en/overview/models.md)
- [Vidau Create Task](https://doc.superaiglobal.com/en/api/create-task.md)
- [Model List API and Capability Validation](references/capabilities.md)
- [Vidau API Error Codes and User Messages](references/errors.md)
- [Vidau Model List and Selection](references/models.md)
- [Create Task Parameters](references/parameters.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks for video and thumbnail URLs, plus concise status, error, or credit summaries derived from API JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VIDAU_API_KEY and network access to Vidau/SuperAI endpoints; generated media links should be copied verbatim from script output.]

## Skill Version(s):

1.0.8 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
