## Description: <br>
Turn a PDF (whitepaper, ebook chapter, slide deck export, research paper) into a short summary video. Use when the source is a PDF URL or a PDF the agent can upload to public storage first. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[api00](https://clawhub.ai/user/api00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and agents use this skill to turn public PDF URLs into 30-90 second summary videos with Revid. It is useful when a user wants a concise video summary of a whitepaper, research paper, slide export, or ebook chapter and can provide a reachable PDF URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF URLs and document contents are sent to Revid for processing. <br>
Mitigation: Use only PDFs approved for external processing; avoid confidential, regulated, proprietary, or personal documents unless that exposure is deliberately approved. <br>
Risk: Local PDFs must be uploaded to public or shared storage before Revid can fetch them. <br>
Mitigation: Prefer time-limited signed URLs or controlled shared storage, and remove uploaded files after processing when possible. <br>
Risk: The skill requires a Revid API key. <br>
Mitigation: Use an environment variable for REVID_API_KEY, prefer a scoped key where available, and avoid exposing the key in prompts, logs, or shared files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/api00/revid-pdf-to-video) <br>
- [Revid Render API Endpoint](https://www.revid.ai/api/public/v3/render) <br>
- [Revid Status API Endpoint](https://www.revid.ai/api/public/v3/status?pid=$PID) <br>
- [Example Payload](examples/whitepaper.json) <br>
- [Example Runner](examples/run.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with HTTP, JSON, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REVID_API_KEY and a public, unauthenticated PDF URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
