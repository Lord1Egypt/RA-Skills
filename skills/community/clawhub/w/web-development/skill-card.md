## Description: <br>
Use when users need to implement, integrate, debug, build, deploy, or validate a Web frontend after the product direction is already clear, especially for React, Vue, Vite, browser flows, or CloudBase Web integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binggg](https://clawhub.ai/user/binggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement, debug, validate, and deploy web frontends, especially React, Vue, Vite, browser flows, and CloudBase Web integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through web app edits that affect user-visible behavior. <br>
Mitigation: Review proposed changes and require the agent to report the build, typecheck, lint, test, or browser validation it performed. <br>
Risk: CloudBase hosting or deployment guidance can affect the wrong environment if the target is ambiguous. <br>
Mitigation: Confirm the target CloudBase environment before deployment or configuration changes, and verify the resulting hosting configuration after the change. <br>
Risk: Browser-flow validation may be incomplete when credentials, backend services, or paid APIs are unavailable. <br>
Mitigation: Require the agent to name any unverified route, interaction, credential, backend, or API dependency before treating the work as complete. <br>


## Reference(s): <br>
- [Web Development Skill Source](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/references/web-development/SKILL.md) <br>
- [CloudBase Main Skill Entry](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/SKILL.md) <br>
- [Browser Validation](artifact/browser-testing.md) <br>
- [Framework Guidance](artifact/frameworks.md) <br>
- [CloudBase Integration Documentation](https://docs.cloudbase.net/integration/introduce/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include implementation steps, validation steps, configuration guidance, and deployment checks.] <br>

## Skill Version(s): <br>
1.27.8 (source: ClawHub release metadata; artifact frontmatter declares 2.23.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
