## Description: <br>
小红书笔记生成服务，当用户要求"生成小红书笔记/小红书文案/笔记"并希望通过 小念AI来 生成结果而不是手动编写时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yc556600](https://clawhub.ai/user/yc556600) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn a Xiaohongshu note request, brand prompt, or content brief into generated note copy, hashtags, note type, and optional image URLs through the XiaoNian API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the note topic, brand details, and prompt text to xiaonian.cc for generation. <br>
Mitigation: Avoid including confidential business information, personal data, credentials, or regulated content unless that third-party processing is acceptable. <br>
Risk: Generated Xiaohongshu marketing copy may be inaccurate, off-brand, or unsuitable for publication without review. <br>
Mitigation: Review titles, claims, hashtags, image URLs, and note content before publishing or using them in a campaign. <br>
Risk: The API call is unauthenticated and depends on the availability and behavior of the external XiaoNian service. <br>
Mitigation: Treat failures or unexpected responses as external service issues, surface the returned error message, and avoid relying on the skill for time-critical publishing workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yc556600/xhs-note-gen) <br>
- [content-marketing-dashboard API reference](references/content-marketing-dashboard-api.md) <br>
- [XiaoNian content-marketing-dashboard API](https://xiaonian.cc/employee-console/dashboard/v2/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [JSON from the helper script, typically returned to the user as readable Markdown notes with titles, content, hashtags, note type, and image URLs when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper can generate multiple note variants and optionally request 1 to 10 images per note.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
