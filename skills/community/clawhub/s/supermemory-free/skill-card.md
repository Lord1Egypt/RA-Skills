## Description: <br>
Cloud knowledge backup and retrieval using Supermemory.ai free tier. Store high-value insights to the cloud and search them back when local memory is insufficient. Uses standard /v3/documents and /v3/search endpoints (no Pro-only features). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Broedkrummen](https://clawhub.ai/user/Broedkrummen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to store selected session knowledge in Supermemory.ai and retrieve it later when local memory is insufficient. It also supports optional daily auto-capture of high-value memory-log entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local session-memory content and search queries may be sent to Supermemory.ai. <br>
Mitigation: Review candidate content before upload, start with auto_capture.py --dry-run, and avoid storing secrets or sensitive locations. <br>
Risk: The cron installer can persist daily uploads from the workspace. <br>
Mitigation: Enable cron only after reviewing the exact upload behavior, and use install_cron.sh --remove when persistent capture is no longer intended. <br>
Risk: The skill requires a bearer API key for Supermemory.ai. <br>
Mitigation: Keep SUPERMEMORY_OPENCLAW_API_KEY in the environment or local .env only, and rotate it if it is exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Broedkrummen/supermemory-free) <br>
- [Supermemory.ai](https://supermemory.ai) <br>
- [Supermemory API base](https://api.supermemory.ai) <br>
- [Supermemory console](https://console.supermemory.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and optional JSON responses from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUPERMEMORY_OPENCLAW_API_KEY; can store, search, dry-run auto-capture, or install a daily cron job.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
