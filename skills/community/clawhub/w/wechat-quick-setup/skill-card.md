## Description: <br>
Generates starter files, cloud function templates, and page templates for WeChat Mini Program projects using Tencent Cloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building WeChat Mini Programs use this skill to initialize project structure and generate Tencent Cloud function and page starter code for login, CRUD, payments, uploads, product listings, and orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated backend templates can create unsafe database behavior if deployed unchanged. <br>
Mitigation: Treat generated backend code as starter code and add server-side authentication, authorization, collection allowlists, ownership checks, input validation, database permissions, and separate development, test, and production environment IDs. <br>
Risk: Payment and order templates may be unsafe if they trust client-provided values. <br>
Mitigation: Validate payment amounts, order IDs, product ownership, and order state on the server before creating or updating payment and order records. <br>
Risk: Upload and messaging templates can expose abuse paths without deployment-specific controls. <br>
Mitigation: Add file type and size limits, recipient authorization checks, rate limits, and logging before enabling uploads or subscription messaging in production. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yang1002378395-cmyk/wechat-quick-setup) <br>
- [Publisher profile](https://clawhub.ai/user/yang1002378395-cmyk) <br>
- [WeChat Mini Program platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and generated JavaScript, WXML, WXSS, and JSON project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files target WeChat Mini Program and Tencent Cloud project structure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
