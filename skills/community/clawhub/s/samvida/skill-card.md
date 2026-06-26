## Description: <br>
Samvida crawls business websites, fills information gaps conversationally, and generates structured, agent-optimized llms.txt files with optional deployment guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ngm9](https://clawhub.ai/user/ngm9) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External business operators and developers use this skill to create an agent-readable llms.txt contract for a website, review gaps in automatically crawled business information, and optionally prepare deployment to supported hosting providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill crawls user-supplied websites and may collect public contact details or business information. <br>
Mitigation: Crawl only sites you own or are authorized to scan, and review the generated llms.txt before publishing. <br>
Risk: Optional deployment can make live Cloudflare or Webflow changes using powerful provider tokens. <br>
Mitigation: Use short-lived, least-privilege deployment tokens, confirm the target domain and provider before deployment, and revoke tokens after use. <br>
Risk: Deployment credentials could be exposed if pasted into ordinary chat or logs. <br>
Mitigation: Handle provider tokens as secrets and avoid pasting them into non-secret channels or persistent logs. <br>
Risk: User-influenced shell commands or deployment steps may affect local files or hosted content. <br>
Mitigation: Review commands and generated files before execution, especially before publishing to a live domain. <br>


## Reference(s): <br>
- [Samvida on ClawHub](https://clawhub.ai/ngm9/samvida) <br>
- [llms.txt Specification](https://llmstxt.org) <br>
- [llms.txt Generation Reference](references/llms_txt_spec.md) <br>
- [Cloudflare, Webflow, and Framer Deployment Reference](references/cloudflare_api.md) <br>
- [Cloudflare API](https://api.cloudflare.com/client/v4) <br>
- [Webflow API](https://api.webflow.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown conversation output with generated llms.txt text and inline shell commands when crawling or deployment is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated llms.txt content to /tmp/samvida_llms.txt when finalizing.] <br>

## Skill Version(s): <br>
0.3.3 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
