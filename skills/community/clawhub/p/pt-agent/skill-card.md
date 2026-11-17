## Description:

PT Agent helps authorized users search private-tracker media, inspect tracker and downloader status, configure supported access methods, and hand selected results to a configured downloader.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xzulab](https://clawhub.ai/user/xzulab)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use PT Agent to operate authorized private-tracker accounts and supported downloaders through natural-language search, account status, configuration, and download-handoff workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private tracker or downloader credentials may be used against broadly configured network endpoints.

Mitigation: Use official HTTPS tracker, API, RSS, Prowlarr, or Jackett endpoints only; keep downloader endpoints local or explicitly trusted; store secrets through supported references instead of chat or plain configuration.

Risk: A selected search result can be sent to the configured downloader and started without a final confirmation.

Mitigation: Review the visible search result before selecting it, configure only trusted default downloaders, and request paused adds when immediate downloading is not intended.

## Reference(s):

- [PT Agent README](README.md)
- [Agent Contract Reference](references/agent-contract.md)
- [Runtime Policy Reference](references/runtime-policy.md)
- [Common Site API Adapter Reference](references/common-site-apis.md)
- [Downloader Integration Reference](references/downloader-integration.md)
- [Adapter Catalog](references/adapter-catalog.json)
- [Site Preset Catalog](references/site-preset-catalog.json)
- [PT-depiler](https://github.com/pt-plugins/PT-depiler)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise natural-language replies with numbered result lists, setup guidance, and occasional inline shell commands when implementation details are requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and queue responses are capped for readability; private URLs, passkeys, cookies, API keys, and raw downloader secrets should not be exposed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
