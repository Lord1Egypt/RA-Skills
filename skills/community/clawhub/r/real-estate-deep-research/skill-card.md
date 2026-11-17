## Description:

DeepLink Agentic helps agents create, monitor, retrieve, and iterate on deep real-estate research tasks through the 深度智联 Agentic service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dichanai](https://clawhub.ai/user/dichanai)

### License/Terms of Use:

MIT-0

## Use Case:

Agents supporting real-estate professionals use this skill to clarify research requests, submit them to DeepLink Agentic, monitor long-running work including human-in-the-loop prompts, and retrieve resulting reports or files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends real-estate prompts, selected uploads, task history, and an account token to agentic.dichanai.com.

Mitigation: Install and run it only when the publisher and service are trusted for that data, and avoid submitting sensitive material unless it is required for the task.

Risk: Token renewal can print a NEW_TOKEN value.

Mitigation: Treat printed token values as secrets and do not include them in public messages, logs, or shared artifacts.

Risk: Share and delete operations can expose or remove task data when used unintentionally.

Mitigation: Use share and delete only after confirming that the resulting disclosure or removal is intended.

Risk: The dependency installation requests an unpinned requests package.

Mitigation: Prefer a pinned dependency or controlled execution environment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dichanai/skills/real-estate-deep-research)
- [ClawHub publisher profile](https://clawhub.ai/user/dichanai)
- [DeepLink Agentic service](https://agentic.dichanai.com)
- [DeepLink Agentic API documentation](https://agentic.apifox.cn/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown responses with inline shell commands, status text, and file or download references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTIC_TOKEN and sends user prompts and selected uploads to agentic.dichanai.com.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
