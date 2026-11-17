## Description:

SkillSentry audits a local OpenClaw install for security posture and prompt-injection indicators and produces a JSON report for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poolguy24](https://clawhub.ai/user/poolguy24)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run local OpenClaw security checks, identify prompt-injection indicators, inspect local status output, and review a JSON security report before deployment or routine operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The UI and documentation can imply always-on protection or alerting that the artifact does not fully implement.

Mitigation: Treat the skill as a local audit helper until the missing backend, configuration, scheduling, and reporting components are implemented and reviewed.

Risk: The JSON audit output can include sensitive matching lines from local memory or skill files.

Mitigation: Review and redact reports before sharing them outside the local environment.

Risk: A fake clean status in the panel can mislead users about current security posture.

Mitigation: Remove or replace static clean-status indicators with results from the actual audit before relying on the panel.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/poolguy24/skills/skillsentry)
- [Frenzy risks & references](artifact/references/threats.md)
- [OWASP GenAI LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [Obsidian Security Agentic AI Security](https://www.obsidiansecurity.com/blog/agentic-ai-security)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON report with shell command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit output may include matching local file lines and local status output; review before sharing.]

## Skill Version(s):

1.1.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
