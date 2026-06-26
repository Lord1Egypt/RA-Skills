## Description: <br>
YouOS is a local-first personal email copilot that learns a user's writing style from Gmail, Google Docs, and WhatsApp exports, then drafts replies in that user's voice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drbaher](https://clawhub.ai/user/drbaher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees use YouOS to install and run a local personal email copilot that drafts replies in their own writing style. It is intended for explicit local setup with Google ingestion credentials and optional external model fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private email, notes, or retrieved context can be sent to Claude when external fallback paths are enabled. <br>
Mitigation: For strict local use, set review.draft_model to local and model.fallback to none before drafting. <br>
Risk: Installation executes local package code and stores sensitive Gmail, Docs, and WhatsApp-derived data on the user's machine. <br>
Mitigation: Review the source and settings before installation, and protect the YOUOS_DATA_DIR SQLite database and related local files. <br>
Risk: Web UI or browser-extension use can expose private drafts if the service is reachable beyond the local user. <br>
Mitigation: Keep the server bound to 127.0.0.1 and configure a PIN/token allowlist before using the web UI or browser extension. <br>
Risk: Background service and nightly processing can continue ingestion, fine-tuning, or autoresearch outside an interactive session. <br>
Mitigation: Enable service or nightly mode only when persistent background processing is intended. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/drbaher/youos) <br>
- [Publisher profile](https://clawhub.ai/user/drbaher) <br>
- [Project homepage](https://github.com/DrBaher/youos) <br>
- [Browser extension](https://github.com/DrBaher/youos/tree/main/extension) <br>
- [Product site](https://youos.drbaher.com/) <br>
- [Privacy policy](PRIVACY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and Markdown with CLI commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces email draft text and local setup/runtime guidance; may reference sensitive local email context when configured by the user.] <br>

## Skill Version(s): <br>
0.1.22 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
