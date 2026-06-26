## Description: <br>
Build and publish complete websites via WebsitePublisher.ai by creating pages, uploading assets, managing dynamic data, configuring contact forms, and publishing to a live URL through conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[megberts](https://clawhub.ai/user/megberts) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, site owners, and agent users use this skill to create, update, and publish WebsitePublisher.ai sites from conversational instructions, including pages, assets, structured content, blog-style data, and contact forms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent using the configured project token can modify and publish website content. <br>
Mitigation: Install the skill only for WebsitePublisher.ai projects the user is comfortable letting an agent modify, and review page, form, and data changes before live publication. <br>
Risk: Project tokens and published content may expose sensitive information if handled carelessly. <br>
Mitigation: Use a dedicated or scoped token when available, keep credentials in environment variables, and avoid storing secrets or sensitive personal data in public pages or MAPI records. <br>


## Reference(s): <br>
- [WebsitePublisher.ai](https://www.websitepublisher.ai) <br>
- [WebsitePublisher.ai API Docs](https://www.websitepublisher.ai/docs) <br>
- [PAPI Docs](https://www.websitepublisher.ai/docs/papi) <br>
- [MAPI Docs](https://www.websitepublisher.ai/docs/mapi) <br>
- [SAPI Docs](https://www.websitepublisher.ai/docs/sapi) <br>
- [ClawHub Skill Page](https://clawhub.ai/megberts/websitepublisher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON, HTML, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses WEBSITEPUBLISHER_TOKEN and WEBSITEPUBLISHER_PROJECT to call WebsitePublisher.ai APIs and may publish changes to a live site.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
