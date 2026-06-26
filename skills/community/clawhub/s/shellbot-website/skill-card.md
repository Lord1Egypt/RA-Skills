## Description: <br>
Builds, deploys, and designs micro apps and websites on Cloudflare Workers, including scaffolding from templates, custom domains, resource provisioning, secret management, and production-grade frontend guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cohnen](https://clawhub.ai/user/cohnen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold, configure, deploy, and operate Cloudflare Workers websites and web apps. It supports common release tasks such as provisioning D1, KV, R2, and Queues, managing secrets, configuring custom domains, and applying frontend design guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent high-impact authority over a Cloudflare account. <br>
Mitigation: Use a narrowly scoped Cloudflare API token and review planned deployment, provisioning, domain, secret, and teardown operations before execution. <br>
Risk: Secret handling and status or log commands may expose sensitive application data. <br>
Mitigation: Avoid passing production secrets as command-line arguments, keep secret files local and access-controlled, and review logs before sharing them. <br>
Risk: Secret deletion and teardown commands can remove application access or deployed services. <br>
Mitigation: Verify target names and environments before destructive commands, and require explicit user approval for secret deletion and teardown actions. <br>


## Reference(s): <br>
- [Shell homepage](https://getshell.ai) <br>
- [ClawHub skill page](https://clawhub.ai/cohnen/shellbot-website) <br>
- [Cloudflare Workers documentation](https://developers.cloudflare.com/workers/) <br>
- [Wrangler CLI documentation](https://developers.cloudflare.com/workers/wrangler/) <br>
- [Cloudflare D1 documentation](https://developers.cloudflare.com/d1/) <br>
- [Cloudflare R2 documentation](https://developers.cloudflare.com/r2/) <br>
- [Cloudflare KV documentation](https://developers.cloudflare.com/kv/) <br>
- [Cloudflare Workers templates](https://developers.cloudflare.com/workers/get-started/quickstarts/) <br>
- [Cloudflare Workers Templates](references/cf-templates.md) <br>
- [Custom Domains for Cloudflare Workers](references/custom-domains.md) <br>
- [Wrangler Configuration Reference](references/wrangler-config.md) <br>
- [Typography](references/typography.md) <br>
- [Color & Contrast](references/color-and-contrast.md) <br>
- [Spatial Design](references/spatial-design.md) <br>
- [Motion Design](references/motion-design.md) <br>
- [Interaction Design](references/interaction-design.md) <br>
- [Responsive Design](references/responsive-design.md) <br>
- [UX Writing](references/ux-writing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, code snippets, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create project files or invoke Cloudflare Wrangler commands when authorized by the user.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
