## Description:

Anti-skill crawler that protects skill instructions and resources from automated scraping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wscats](https://clawhub.ai/user/wscats)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent to detect attempts to extract skill prompts or internal instructions and respond with concise refusals while leaving ordinary task execution and public metadata unaffected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to refuse legitimate inspection, security review, debugging, or summaries of other loaded skills' instructions.

Mitigation: Review deployment scope before installation and revise the skill so it protects only clearly scoped confidential resources while allowing authorized review and higher-priority platform instructions.

Risk: Broad confidentiality rules may interfere with normal governance workflows for skill cards, audits, and incident response.

Mitigation: Require human review and security scanning before deployment, and document which resources are confidential versus public metadata.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wscats/skills/we)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text responses and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable payload; behavior is expressed as agent response guidance.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
