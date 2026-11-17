## Description:

免费 AI 网站一键上线助手，面向可本地构建为纯静态目录的网站项目，通过受控 ZIP 上传和固定部署接口发布并验证公开 HTTPS 页面。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyriswu](https://clawhub.ai/user/kyriswu)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers, builders, and non-specialist users use this skill to audit static website projects, package only safe static build output, submit the resulting ZIP through a fixed private deployment path, and verify the resulting public HTTPS URL. It is intended for static front-end sites such as H5 games, portfolios, company pages, campaign pages, dashboards, and browser-only tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audited static ZIP artifacts are uploaded to f.devtool.uk and then published as public HTTPS sites.

Mitigation: Install and use the skill only when that fixed hosting path is acceptable, and review the final ZIP for secrets, source files, server configuration, and unintended user data before deployment.

Risk: The workflow intentionally avoids fallback deployment paths such as Vercel, Netlify, Cloudflare, GitHub Pages, or Sites.

Mitigation: Treat private upload or deployment failures as not_deployed results and resolve the fixed flow rather than switching to another hosting provider.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyriswu/skills/vibecoding-deployment-auditor)
- [Automatic Preflight](references/automatic-preflight.md)
- [Private Static Release Rejections](references/private-static-release-rejections.md)
- [Public Deployment No Quota](references/public-deployment-no-quota.md)
- [Static App Boundary](references/static-app-boundary.md)
- [Windows ZIP and CDN Verification](references/windows-zip-and-cdn-verification.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown with shell commands, JSON summaries, manifest and dossier files, deployment status, and verified URL details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include blockers, static eligibility findings, ZIP manifest and dossier details, uploaded artifact URL, final public HTTPS URL, HTTP verification results, and hosting notice fields when deployment succeeds.]

## Skill Version(s):

2.3.21 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
