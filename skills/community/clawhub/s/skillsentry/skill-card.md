## Description: <br>
SkillSentry audits a local OpenClaw install for security posture, prompt-injection indicators, gateway status, cron exposure, and local port findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Poolguy24](https://clawhub.ai/user/Poolguy24) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and OpenClaw operators use this skill to run local checks for prompt-injection indicators, gateway status, session status, and unexpected localhost ports. It produces a JSON report for review and alerting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The panel can show a clean result without performing a real scan. <br>
Mitigation: Run the CLI audit script against the intended WORKDIR and OUTDIR, then review the generated JSON report before relying on scan status. <br>
Risk: JSON reports may include sensitive status output or prompt-injection snippets. <br>
Mitigation: Review and redact generated reports before sharing them outside the local security review workflow. <br>
Risk: Recurring cron scans create persistent local scheduled activity. <br>
Mitigation: Enable cron only deliberately, document the configured cadence, and retain instructions for disabling the schedule. <br>


## Reference(s): <br>
- [Frenzy risks and references](artifact/references/threats.md) <br>
- [OWASP GenAI LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) <br>
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) <br>
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) <br>
- [Obsidian Security Agentic AI Security](https://www.obsidiansecurity.com/blog/agentic-ai-security) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON report with Markdown and shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The audit script prints JSON to stdout and can be redirected to a report file.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
