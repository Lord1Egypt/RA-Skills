## Description: <br>
Fetch and interpret Rankscale GEO (Generative Engine Optimization) analytics, including brand visibility score, citation rate, sentiment, and top AI search terms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mathias-RS](https://clawhub.ai/user/Mathias-RS) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing, SEO, communications, and developer teams use this skill to query Rankscale account analytics and turn AI-search visibility, citation, sentiment, and content-gap metrics into actionable reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers and API-key handling could expose Rankscale account analytics or credentials unintentionally. <br>
Mitigation: Configure the key through OpenClaw-managed environment secrets or a protected .env file, avoid the --api-key flag, treat terminal output as sensitive, rotate leaked keys, and use explicit Rankscale-branded prompts. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/Mathias-RS/rs-geo-analytics) <br>
- [Rankscale homepage](https://rankscale.ai) <br>
- [API Endpoint Clarification](API_ENDPOINT_CLARIFICATION.md) <br>
- [Commands Reference](references/COMMANDS.md) <br>
- [Features Guide](references/FEATURES.md) <br>
- [Usage Guide](USAGE.md) <br>
- [Architecture](docs/ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with ASCII report blocks and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Rankscale PRO account API access and RANKSCALE_API_KEY configuration.] <br>

## Skill Version(s): <br>
1.0.11 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
