## Description: <br>
Report Expert generates HTML report pages, maintains a Cloudflare Pages site, checks and repairs page structure, and verifies deployed results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomtrije](https://clawhub.ai/user/tomtrije) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to turn HTML, Markdown, URLs, or plain text into structured report pages and publish them to an existing Cloudflare Pages site. It also supports site index maintenance, remote synchronization, and deployment verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish untrusted or incorrect HTML to a live Cloudflare Pages site. <br>
Mitigation: Review generated HTML and report content before publishing, and run the built-in structure checks and deployment verification before relying on the live page. <br>
Risk: Cloudflare deployment uses live credentials and can change or remove production content. <br>
Mitigation: Use a least-privilege Cloudflare API token scoped to the intended Pages project and confirm remove, sync, and publish commands before execution. <br>
Risk: Remote synchronization and URL ingestion can pull content from an untrusted or compromised site. <br>
Mitigation: Only synchronize from trusted site URLs and review fetched content and index changes before redeploying. <br>


## Reference(s): <br>
- [Report Expert on ClawHub](https://clawhub.ai/tomtrije/report-expert) <br>
- [Report Expert Published Site](https://report-expert-skill.pages.dev) <br>
- [Chart and Visualization Specification](references/chart-spec.md) <br>
- [Deployment Checklist](references/checklist.md) <br>
- [Design Specification](references/design-spec.md) <br>
- [Verification Details](references/verify-detail.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated HTML/CSS/JavaScript/Python files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates deployable report-site files, index metadata, Cloudflare Pages deployment commands, and verification guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact manifest, updated 2026-06-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
