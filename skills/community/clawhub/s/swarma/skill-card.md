## Description: <br>
Agent teams that run growth experiments and build their own playbook using the GROWS loop: generate hypothesis, run experiment, observe signal, weigh verdict, and stack playbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glitch-rabin](https://clawhub.ai/user/glitch-rabin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Growth teams, founders, marketers, and agent developers use this skill to set up and operate swarma experiment teams for hooks, landing pages, outreach, pricing, activation, retention, and other AARRR funnel work. The skill guides agents through CLI setup, team creation, experiment cycles, metric logging, and playbook review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and operates an external swarma CLI and uses OpenRouter for LLM-powered growth experiment cycles. <br>
Mitigation: Install only when that external CLI and OpenRouter dependency are acceptable, and use a restricted OpenRouter API key. <br>
Risk: Experiment metrics and context may contain sensitive business or customer information. <br>
Mitigation: Review metrics and context before import, and avoid adding sensitive data unless the deployment environment is approved for it. <br>
Risk: MCP, REST, and continuous run modes can keep services or agent cycles active longer than intended. <br>
Mitigation: Use those modes only when operators know how to stop them and can restrict access to the running service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/glitch-rabin/swarma) <br>
- [swarma website](https://swarma.dev) <br>
- [swarma repository metadata](https://github.com/glitch-rabin/swarma) <br>
- [OpenRouter API keys](https://openrouter.ai/keys) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code] <br>
**Output Format:** [Markdown guidance with CLI commands, JSON/YAML configuration snippets, and CSV examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires terminal access and OPENROUTER_API_KEY for LLM-powered agent cycles.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
