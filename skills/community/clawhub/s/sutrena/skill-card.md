## Description: <br>
Deploy websites, landing pages, forms, and dashboards through Sutrena's hosted REST API without git, hosting setup, or a build step. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaichogami](https://clawhub.ai/user/kaichogami) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Sutrena to publish pages, lead capture forms, waitlists, hosted forms, and dashboards directly from an agent conversation without setting up hosting or a build pipeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create live public pages and hosted forms. <br>
Mitigation: Review generated content before publication and only publish material intended to be public. <br>
Risk: Site, form, dashboard, and collected-submission data may be sent to Sutrena. <br>
Mitigation: Do not submit secrets, regulated personal data, or sensitive business data unless the user has approved that use. <br>
Risk: Sutrena API keys authorize publishing and account operations. <br>
Mitigation: Use a Sutrena-specific API key when available and never expose API keys in generated HTML or client-side JavaScript. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaichogami/sutrena) <br>
- [Sutrena homepage](https://sutrena.com) <br>
- [Sutrena agent reference](https://sutrena.com/llms-full.txt) <br>
- [Sutrena API schema](https://sutrena.com/api/schema) <br>
- [Sutrena OpenAPI spec](https://sutrena.com/api/openapi.json) <br>
- [Sutrena guides](https://sutrena.com/guides) <br>
- [Sutrena templates](https://sutrena.com/templates) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with live URLs, generated page or form content, and JSON API payloads when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create public pages, hosted forms, dashboards, webhooks, subdomains, uploaded assets, and custom-domain configuration through Sutrena APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
