## Description: <br>
Automatically analyzes websites for performance metrics and audit issues using Lighthouse. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LJ-Hao](https://clawhub.ai/user/LJ-Hao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run local Lighthouse audits against website URLs, review performance, accessibility, SEO, and best-practice scores, and turn failing metrics into actionable fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens user-supplied sites in local Chrome automation with the Chrome sandbox disabled. <br>
Mitigation: Audit sites you control where possible, isolate sensitive targets, and remove or avoid the --no-sandbox flag when feasible. <br>
Risk: Saved Lighthouse reports can contain URL structure or other sensitive details from analyzed pages. <br>
Mitigation: Avoid authenticated or sensitive internal URLs unless isolated, and review or redact saved reports before retaining them in memory or sharing them. <br>
Risk: The release security verdict is suspicious and calls for review before installation. <br>
Mitigation: Install only if comfortable running local Node/npm code and Chrome automation, and review the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/LJ-Hao/web-auto-analyzer) <br>
- [Homepage](https://github.com/user/chrome-devtools-auto-analyzer) <br>
- [Quick Start](quick-start.md) <br>
- [Setup Guide](setup.md) <br>
- [Metrics Reference](metrics-reference.md) <br>
- [Audit Checklist](audit-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tables, inline code, shell commands, and optional JSON/HTML Lighthouse report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save audit reports under ./results/ and may track summary history only after user confirmation.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
