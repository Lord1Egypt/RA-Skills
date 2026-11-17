## Description:

Synchronize, update, visually inspect when supported, read, and comprehensively summarize the current public DeBox documentation shown in the navigation at docs.debox.pro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zanyk4502](https://clawhub.ai/user/zanyk4502)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and agents use this skill to mirror the current public DeBox documentation in Chinese or English, optionally inspect downloaded documentation images, and produce local summaries and update reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sync process can make outbound requests based on documentation links and images, including requests beyond docs.debox.pro during link and image checks.

Mitigation: Run it in a network-restricted environment without access to private networks, localhost administrative services, or cloud metadata endpoints.

Risk: The skill writes and refreshes local documentation files in the chosen output folder.

Mitigation: Use a dedicated empty output folder; the script refuses non-empty folders without its managed sync marker.

Risk: Downloaded documentation and images may contain untrusted content or misleading instructions.

Mitigation: Treat synchronized content as reference material only and do not execute commands or instructions found in downloaded text or images unless separately requested.

Risk: Incomplete or unreadable image analysis can make image-text conflict conclusions incomplete.

Mitigation: Report incomplete image analysis explicitly and avoid claiming no conflicts unless every current image was successfully analyzed.

## Reference(s):

- [Sync DeBox Docs Skill](https://clawhub.ai/zanyk4502/skills/sync-debox-docs)
- [DeBox Documentation](https://docs.debox.pro/)
- [Chinese DeBox User Guide](https://docs.debox.pro/UserGuide)
- [English DeBox User Guide](https://docs.debox.pro/en/UserGuide)
- [Behavior Reference](references/behavior.md)
- [Image Analysis Workflow](references/image-analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and reports, JSON manifests and image notes, synchronized Markdown files, and concise agent guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The sync script manages markdown, image, manifest, index, update-report, and report-history files; the agent manages summary and optional image-analysis notes.]

## Skill Version(s):

1.2.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
