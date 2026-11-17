## Description:

Parses PDF and image documents through a remote document parsing service and returns extracted text, tables, and formulas as Markdown or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[va-ais](https://clawhub.ai/user/va-ais)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and OpenClaw users use vaDocparse to extract text, tables, and formulas from PDFs and supported image files through a configured document parsing MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Readable local documents may be uploaded to a remote parsing service.

Mitigation: Use only an approved service endpoint, prefer HTTPS, and avoid sensitive documents unless retention and network handling are understood.

Risk: Service credentials may be stored in local configuration.

Mitigation: Keep real API keys out of command lines, logs, dry-run output, and broadly readable .env or OpenClaw configuration files.

Risk: The parsing service and network path are required for successful operation.

Mitigation: Deploy only where the remote parsing service is trusted and reachable, and surface coded failures without exposing backend service details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/va-ais/skills/va-docparse)
- [Publisher profile](https://clawhub.ai/user/va-ais)
- [Skill documentation](artifact/SKILL.md)
- [MCP client source](artifact/mcp/docparse.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files]

**Output Format:** [Markdown or JSON document parsing results, plus concise status or coded error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports PDF and image inputs; successful parses are saved to a local output file and should expose a download path.]

## Skill Version(s):

1.0.1 (source: evidence.json release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
