## Description: <br>
Stuff Skill - 秩。告诉 AI 你想管理什么,它给你生成一个专属 App。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirayang-max](https://clawhub.ai/user/kirayang-max) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to turn a natural-language description of a personal collection, inventory, log, or checklist into a local-first or Cloudflare-synced PWA with fields, UI, import/export, and deployment guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated cloud backend templates may expose personal data publicly when deployed without authentication or with permissive CORS. <br>
Mitigation: Add authentication and authorization, restrict CORS to trusted origins, and verify data storage and retention before using the generated backend with real personal data. <br>
Risk: Generated destructive operations may modify or delete user records if deployed without review. <br>
Mitigation: Review and harden destructive endpoints and keep import/export backups available before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kirayang-max/skills/stuff-skill) <br>
- [Scenario Inspiration](references/inspiration.md) <br>
- [Field Inference Rules](references/field-inference.md) <br>
- [Design Proposal Guide](references/design-proposal.md) <br>
- [UI Component Specification](references/components.md) <br>
- [Cloudflare Pages and D1 Deployment Guide](references/deploy-guide.md) <br>
- [Validation Rules](references/validation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with generated HTML, CSS, JavaScript, JSON, YAML, SQL, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local mode produces PWA files; cloud mode may add Cloudflare Pages Functions, D1 configuration, a service worker, and icon assets.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
