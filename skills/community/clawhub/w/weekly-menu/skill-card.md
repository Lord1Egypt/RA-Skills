## Description: <br>
Generates a weekly meal plan with images, recipe links, shopping support, and a formatted Feishu document based on Xiaohongshu recipe inspiration and user meal preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BeginnerRudy](https://clawhub.ai/user/BeginnerRudy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill through an agent to plan a week of home cooking, collect recipe inspiration from Xiaohongshu, generate a Feishu menu document, and maintain menu history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Feishu credentials and document permissions while creating and editing documents. <br>
Mitigation: Use a least-privilege Feishu app and folder, confirm the target user before granting access, and avoid storing reusable tokens in MEMORY.md. <br>
Risk: The referenced Feishu guide includes delete and move document operations that are broader than weekly menu creation. <br>
Mitigation: Do not permit delete or move calls unless the user explicitly requests that exact operation. <br>
Risk: The skill searches Xiaohongshu, downloads images, and stores meal preference and history data. <br>
Mitigation: Review selected sources and downloaded image files before inserting them, and keep meal profiles and history limited to data needed for planning. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/BeginnerRudy/weekly-menu) <br>
- [Feishu Document Creation Recipe Guide](references/feishu-doc-recipe.md) <br>
- [User Profile Template](references/profile-template.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and chat text with Feishu document links, shell command examples, and YAML configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates Feishu documents, downloads representative images, and appends meal history when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
