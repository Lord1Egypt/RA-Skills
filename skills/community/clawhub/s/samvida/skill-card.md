## Description:

Samvida crawls a business website, fills gaps conversationally, and generates a structured agent-optimized llms.txt file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ngm9](https://clawhub.ai/user/ngm9)

### License/Terms of Use:

MIT

## Use Case:

Business owners, marketers, and developers use Samvida to make a website agent-readable by producing a structured llms.txt file and optionally deploying it to supported hosting providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill crawls arbitrary URLs from the agent's network environment.

Mitigation: Use it only for sites you own or are authorized to manage, and avoid running it from a network that can reach sensitive internal services.

Risk: Deployment-capable Cloudflare or Webflow credentials can change live website hosting.

Mitigation: Use short-lived least-privilege tokens, review /tmp/samvida_llms.txt before deployment, and revoke tokens after use.

Risk: Crawled pages may contain public contact details that are included in the generated llms.txt and sent to the configured OpenClaw LLM provider.

Mitigation: Review the crawled content and generated file before sharing or deploying, and avoid adding sensitive or non-public pages as crawl inputs.

## Reference(s):

- [Samvida ClawHub listing](https://clawhub.ai/ngm9/skills/samvida)
- [llms.txt specification](references/llms_txt_spec.md)
- [Deployment reference for Cloudflare, Webflow, and Framer](references/cloudflare_api.md)
- [llmstxt.org](https://llmstxt.org)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown llms.txt content with deployment commands or platform guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated llms.txt to /tmp/samvida_llms.txt; deployment can update Cloudflare Workers or Webflow when credentials are supplied.]

## Skill Version(s):

0.3.3 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
