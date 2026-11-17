## Description:

Fully conversational remote job finder for WhatsApp powered by Remote Rocketship that uses the rr_jobs_search tool and supports pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lior539](https://clawhub.ai/user/lior539)

### License/Terms of Use:


## Use Case:

External users use this skill in OpenClaw or WhatsApp chat to search remote job listings, refine filters, paginate results, and optionally monitor for new matches. Server administrators use its bundled instructions to install the required rr_jobs_search gateway extension and configure RR_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server install can overwrite shared OpenClaw extension files.

Mitigation: Back up any existing ~/.openclaw/extensions/openclaw.plugin.json and index.ts before deployment, then review the extension files before restarting the gateway.

Risk: RR_API_KEY is required for server-side job search access.

Mitigation: Store RR_API_KEY as an admin-only server secret and do not request or expose it in user chat.

Risk: Job text and links come from an external service and may be inaccurate or unsafe.

Mitigation: Treat returned job content and links as untrusted third-party content and review them before acting on applications or external URLs.

Risk: Ongoing monitoring and profile memory are under-scoped.

Mitigation: Require explicit user opt-in for monitoring and provide clear stop or status controls.

## Reference(s):

- [Remote Jobs Finder ClawHub Page](https://clawhub.ai/lior539/skills/remote-jobs-finder)
- [Remote Rocketship](https://www.remoterocketship.com)
- [Remote Rocketship OpenClaw Jobs API](https://www.remoterocketship.com/api/openclaw/jobs)
- [Artifact README](artifact/README.md)
- [Server Install Notes](artifact/INSTALL_SERVER.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [WhatsApp-friendly Markdown with job listing bullets and installation command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to concise result batches and supports paginated follow-up requests.]

## Skill Version(s):

1.6.2 (source: server release metadata; artifact frontmatter reports 1.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
