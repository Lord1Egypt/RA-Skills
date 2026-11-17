## Description:

Control and monitor Snapmaker 2.0 3D printers via their HTTP API for status, job management, progress watching, and event monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:


## Use Case:

Developers, makers, and printer operators use this skill to discover Snapmaker 2.0 printers, inspect status, monitor print progress, and manage print jobs over the printer's local HTTP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Physical printer controls may execute immediately, and the server security summary notes that some state-changing actions can run even though the documentation describes confirmation prompts.

Mitigation: Review pause, resume, stop, send, and start actions before allowing an agent to invoke them, especially when the printer is shared or actively printing.

Risk: The skill uses a printer token in config.json and sends it to a LAN printer API.

Mitigation: Treat config.json as a secret, keep the printer on a trusted LAN, and avoid exposing the printer API on untrusted networks.

Risk: File upload and print-start actions can cause the printer to act on local model files.

Mitigation: Limit uploaded files to intended print assets and confirm printer readiness before sending or starting a job.

## Reference(s):

- [Snapmaker 2.0 HTTP API Notes](references/API_NOTES.md)
- [Snapmaker Forum: API Documentation](https://forum.snapmaker.com/t/documentation-of-the-web-api/20976/16)
- [Snapmaker Forum: Automatic Start Guide](https://forum.snapmaker.com/t/guide-automatic-start-via-drag-drop/29177)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [CLI text and JSON responses with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and the requests library; expects a workspace snapmaker/config.json containing printer IP, port, and token.]

## Skill Version(s):

1.2.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
