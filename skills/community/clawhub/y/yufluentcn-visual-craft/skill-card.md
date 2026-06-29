## Description: <br>
Yufluent Clawhub Publish Yufluentcn Visual Craft helps agents request Yufluent cloud output for ecommerce A+ page structures, video storyboard scripts, main-image differentiation briefs, and image compliance checklists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, ecommerce operators, and agent workflows use this skill to send product and listing details to the Yufluent service and receive Markdown planning content for Amazon, Shopify, or TikTok visual assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends TOKENAPI_KEY and user-provided product, listing, and brief content to a configurable Yufluent endpoint. <br>
Mitigation: Use only trusted HTTPS TOKENAPI_BASE_URL values, avoid non-HTTPS remote endpoints, and protect TOKENAPI_KEY as a billing credential. <br>
Risk: Generated visual plans, scripts, or compliance checklists may still require marketplace and advertising review. <br>
Mitigation: Review outputs against the target platform policies and applicable advertising requirements before using them in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluentcn-visual-craft) <br>
- [Publisher profile](https://clawhub.ai/user/metahuan) <br>
- [Yufluent homepage](https://claw.changzhiai.com) <br>
- [Yufluent OpenClaw setup](https://claw.changzhiai.com/app/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown plans, briefs, scripts, and checklists returned through a CLI or cloud API call] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not generate image or video files; requires TOKENAPI_KEY and may send product, listing, and brief content to a configurable Yufluent API endpoint.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
