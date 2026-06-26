## Description: <br>
Generate QR codes for any string or URL using the QRClaw open source service, returning terminal-friendly UTF-8 QR text and a hosted smart link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emg110](https://clawhub.ai/user/emg110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to turn public or intentionally shared strings, URLs, payment URIs, app deep links, WiFi credentials, vCards, or workflow-generated URIs into scannable QR codes. It supports both terminal/web presentation with UTF-8 QR blocks and social-channel sharing through a hosted smart link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends input text to an external QR service and makes the generated QR available through a temporary public link. <br>
Mitigation: Use the skill only for data the user is comfortable sending to qrclaw.goplausible.xyz and exposing through a public smart link. <br>
Risk: Sensitive secrets, credentials, private keys, recovery phrases, personal identifiers, or tokens could be exposed if submitted as QR input. <br>
Mitigation: Check inputs before use and refuse requests that appear to include sensitive or private data. <br>
Risk: Frequent automated requests may hit the documented 5 QR codes per minute per IP rate limit. <br>
Mitigation: Avoid tight loops, batch requests conservatively, and wait before retrying when rate limited. <br>


## Reference(s): <br>
- [QR Claw on ClawHub](https://clawhub.ai/emg110/qrclaw) <br>
- [QRClaw API endpoint](https://qrclaw.goplausible.xyz/?q=<url-encoded-string>) <br>
- [QRClaw source link declared by skill](https://github.com/GoPlausible/qrclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown with JSON API response fields, a hosted smart link, and optional UTF-8 QR text in a code block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated QR smart links expire after 24 hours; the service is rate limited to 5 QR codes per minute per IP.] <br>

## Skill Version(s): <br>
1.2.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
