## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wechatgpt798](https://clawhub.ai/user/wechatgpt798)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to drive headless browser workflows through the agent-browser CLI, including navigation, ref-based interaction, state checks, session isolation, screenshots, PDFs, and saved browser state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved auth state, cookies, and storage output can expose account credentials or session access.

Mitigation: Keep saved browser state out of repositories and logs, restrict file permissions, use test or least-privilege accounts where possible, and delete saved auth files when no longer needed.

Risk: The skill depends on an external browser automation CLI.

Mitigation: Install only when browser automation is needed and the external agent-browser CLI source is trusted.

## Reference(s):

- [Wayne Agent Browser on ClawHub](https://clawhub.ai/wechatgpt798/skills/wayne-agent-browser)
- [agent-browser CLI homepage](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the external agent-browser CLI; documented commands can save browser state, cookies, storage data, screenshots, and PDFs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
