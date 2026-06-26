## Description: <br>
Sync your OpenClaw agent with the ScanWow iOS app. Receive high-quality OCR scans from your phone directly into your agent's workspace via a secure webhook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brandons7](https://clawhub.ai/user/brandons7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to receive OCR text from ScanWow iOS scans through a secure webhook and save the text into an agent workspace for filing, extraction, or follow-on workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A publicly exposed webhook or weak bearer token could allow unauthorized scan submissions. <br>
Mitigation: Use a strong random SCANWOW_TOKEN, keep the server bound to localhost, and expose it only through a trusted HTTPS tunnel. <br>
Risk: OCR text may contain sensitive or incorrect content that should not automatically drive agent actions. <br>
Mitigation: Review scanned text before allowing automated workflows to act on it, and choose SCANWOW_DIR deliberately. <br>
Risk: Incoming payloads write files into the agent workspace. <br>
Mitigation: Keep payload size limits, filename sanitization, and a controlled scan output directory in place. <br>


## Reference(s): <br>
- [ScanWow Sync on ClawHub](https://clawhub.ai/brandons7/scanwow-sync) <br>
- [ScanWow on the App Store](https://apps.apple.com/app/scanwow/id6670425738) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Webhook setup guidance for local text-file output from OCR payloads] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
