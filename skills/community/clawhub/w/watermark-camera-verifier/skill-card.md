## Description: <br>
Verifies Today's Watermark Camera photo URLs by submitting public image links to openapi.xhey.top and returning authenticity verdicts with capture time and location metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanmeishijie618](https://clawhub.ai/user/wanmeishijie618) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business teams use this MCP skill to verify whether Today's Watermark Camera photos are authentic and to surface capture time and location metadata for insurance, attendance, construction, evidence, and compliance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided public photo URLs to openapi.xhey.top and can expose returned capture time and location metadata to the agent. <br>
Mitigation: Submit only approved public image links, avoid private, internal, or presigned URLs, and treat returned location/time data as sensitive. <br>
Risk: The skill requires TRUTU_GROUP_KEY and TRUTU_GROUP_SECRET credentials. <br>
Mitigation: Store credentials in environment variables, rotate them when required, and use limited credentials where possible. <br>
Risk: The bundled Feishu implementation contains verbose request and result logging behavior. <br>
Mitigation: Remove or disable verbose logging before using that implementation with real photos or production credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanmeishijie618/watermark-camera-verifier) <br>
- [Publisher profile](https://clawhub.ai/user/wanmeishijie618) <br>
- [Project homepage](https://github.com/wanmeishijie618/trutu-photo-verify-mcp) <br>
- [Trutu build API documentation](https://docs.xhey.top/docs/trutu-build-api) <br>
- [Skill README](README.md) <br>
- [Trutu API reference](trutu-api-reference/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance, configuration] <br>
**Output Format:** [MCP text content containing formatted JSON verification results, plus Markdown setup guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns task IDs, per-photo verdicts, status codes, and capture metadata when available.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
