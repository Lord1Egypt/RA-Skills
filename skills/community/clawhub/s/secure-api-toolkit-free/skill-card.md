## Description: <br>
Secure Api Toolkit Free helps agents call third-party APIs through placeholder-based credential proxying, so local scripts do not need to expose real API keys or OAuth tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to prepare and run CLI-based third-party API calls that replace credentials with placeholders and rely on an external proxy to inject the real tokens. It is aimed at local development, testing, and API connectivity checks for individual developers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes API requests through an external proxy service that can see and forward request data. <br>
Mitigation: Use it only when that proxy relationship is intentional, separate development and production credentials, and revoke provider or machine authorization when finished. <br>
Risk: The artifact recommends a global npm install with an unpinned latest version for the CLI package. <br>
Mitigation: Verify the CLI package and publisher before installation and prefer a pinned, reviewed package version. <br>
Risk: Persistent machine authorization can continue after setup if it is not managed. <br>
Mitigation: Review authorized providers and machines regularly, protect the local machine key directory, and revoke unused authorizations promptly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/secure-api-toolkit-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include secure-curl examples, placeholder conventions, setup steps, operational cautions, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
