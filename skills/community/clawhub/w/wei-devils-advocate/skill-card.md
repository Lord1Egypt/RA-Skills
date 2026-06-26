## Description: <br>
Stress-tests ideas with multiple LLMs in adversarial roles to generate counterarguments, cross-check reasoning, and expose hidden risks and failure modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikehankk](https://clawhub.ai/user/mikehankk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and decision makers use this skill to adversarially test product, investment, strategy, technical, social, scientific, and creative ideas before relying on them. It is designed for risk analysis and decision validation, not consensus seeking or brainstorming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted ideas and generated critiques are sent to configured external LLM providers. <br>
Mitigation: Use only approved provider configurations for sensitive work and avoid submitting confidential content unless the provider and account controls are appropriate. <br>
Risk: The skill requires sensitive provider credentials such as OpenRouter, DashScope, or Bailian API keys. <br>
Mitigation: Store keys in environment variables or a secured .env file, rotate exposed credentials, and avoid committing secrets to shared repositories. <br>
Risk: Intermediate model responses and final reports may be saved locally in plaintext. <br>
Mitigation: Delete or secure generated intermediate and report files after sensitive analyses. <br>
Risk: Adversarial model outputs can still be incomplete, incorrect, or overly confident. <br>
Mitigation: Treat the report as decision-support material and require human review before using it for high-stakes business, financial, technical, or safety decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikehankk/wei-devils-advocate) <br>
- [Bun runtime](https://bun.sh) <br>
- [Bun environment variables documentation](https://bun.sh/docs/runtime/env) <br>
- [Devil's Advocate preview](https://www.bigbigai.com/agent/devils-advocate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown/text report with thesis, hidden assumptions, counterarguments, failure scenarios, survivability, verdict, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured LLM provider API keys and may save plaintext intermediate outputs and reports locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
