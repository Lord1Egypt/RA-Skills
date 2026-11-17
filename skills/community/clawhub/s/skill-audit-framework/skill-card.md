## Description:

Structured security and quality audit framework for AI agent skills. Teaches you what to check before installing any skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enawareness](https://clawhub.ai/user/enawareness)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent users use this skill to guide manual review of ClawHub and MCP skills before installation, covering identity, permissions, behavior, credentials, persistence, and supply-chain concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit verdicts may be treated as a guarantee of safety.

Mitigation: Use the skill's PASS/WARN/FAIL output as review guidance and inspect high-privilege or sensitive skills directly before installation.

Risk: The skill reads and summarizes skill files during audits, which may expose sensitive content if the reviewed files contain secrets.

Mitigation: Review files in an appropriate workspace and avoid placing secrets in skill artifacts.

## Reference(s):

- [Declared Project Homepage](https://github.com/ENAwareness/skill-auditor)
- [Snyk ToxicSkills Research](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- [Koi ClawHavoc Report](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting)
- [ClawHub Skill Page](https://clawhub.ai/enawareness/skills/skill-audit-framework)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report with PASS/WARN/FAIL verdicts and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only guidance; no executable code, credential requests, or tool calls are included in the artifact.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
