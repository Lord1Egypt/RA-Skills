## Description: <br>
Tracks Xiaohongshu daily viral-note rankings by keyword or category, analyzes title and content patterns, and helps creators and operators identify emerging content opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, brand operators, MCN scouts, and growth analysts use this skill to query Xiaohongshu TOP50 breakout notes, review engagement-growth signals, extract reusable topic and title patterns, and optionally generate a shareable HTML report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and queries RedFox/Xiaohongshu data. <br>
Mitigation: Provide REDFOX_API_KEY through the current session or a secret store, and confirm the key source, scope, expiry, and reset options before use. <br>
Risk: API-key setup may involve shell profile files. <br>
Mitigation: Review setup steps before allowing persistent shell-startup changes; prefer temporary environment variables unless permanent configuration is intended. <br>
Risk: Generated HTML loads export libraries from public CDNs. <br>
Mitigation: Use generated HTML only where external CDN loading is acceptable, or replace those libraries with reviewed local copies before distribution. <br>
Risk: Subscription use can create recurring daily output. <br>
Mitigation: Enable subscription only when recurring 19:30 ranking output is desired and cancel it when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/if530770/xhs-daily-ranking) <br>
- [Core workflow](references/core_workflow.md) <br>
- [README](README.md) <br>
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFox service](https://redfox.hk) <br>
- [RedFox Xiaohongshu data endpoint](https://redfox.hk/story/api/cozeSkill/getXhsCozeSkillDataOne) <br>
- [html2canvas CDN dependency](https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) <br>
- [jsPDF CDN dependency](https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, HTML, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables and analysis text, with optional standalone HTML report output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY for live data retrieval; optional HTML reports can be exported to PDF.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
