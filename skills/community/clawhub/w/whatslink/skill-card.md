## Description: <br>
WhatsLink queries metadata for public download, magnet, or torrent links and reports a concise summary with screenshot URLs without downloading or opening content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[violin321](https://clawhub.ai/user/violin321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect public, non-sensitive links through the WhatsLink metadata API before deciding whether content is worth opening or downloading. It is intended for summaries of names, file types, sizes, counts, and optional screenshot URLs, not for downloading target content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitting a private, signed, tokenized, internal, or confidential URL would disclose that link to WhatsLink or the configured compatible endpoint. <br>
Mitigation: Use the skill only with public, non-sensitive URLs and reject links that contain tokens, credentials, internal hosts, or confidential material. <br>
Risk: Screenshot URLs returned by the metadata service can expose sensitive visual content. <br>
Mitigation: Default behavior lists screenshot URLs without downloading or opening them; use --no-screenshots or --max-screenshots 0 when screenshot exposure is not appropriate. <br>
Risk: The metadata API may return unknown, empty, incomplete, or failed results. <br>
Mitigation: Report only the returned metadata and avoid inferring file contents when the service does not identify useful information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/violin321/whatslink) <br>
- [WhatsLink homepage](https://whatslink.info/) <br>
- [WhatsLink API endpoint](https://whatslink.info/api/v1/link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Human-readable text summary or JSON from the helper script, with guidance that may include shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default summaries list screenshot URLs without downloading or opening them; --json returns the raw WhatsLink API response.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release metadata and helper user-agent) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
