## Description: <br>
Structured security and quality audit framework for AI agent skills. Teaches you what to check before installing any skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enawareness](https://clawhub.ai/user/enawareness) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and agent users use this skill to guide pre-install reviews of ClawHub and MCP skills across identity, permissions, behavior, credential handling, side effects, and dependency risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security guidance describes sensitive, purpose-aligned browser automation and API-key configuration in the release evidence. <br>
Mitigation: Install only when you trust the referenced bridge, keep any API key secret, and review high-impact browser actions before applying them. <br>
Risk: This skill provides a review framework rather than a deterministic scanner or sandbox. <br>
Mitigation: Use its report as a structured checklist and manually review high-privilege skill source files before installing them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/enawareness/skill-audit-framework) <br>
- [Snyk ToxicSkills research](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) <br>
- [Koi ClawHavoc incident report](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown audit report with PASS/WARN/FAIL verdicts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a six-domain review checklist and flagged-item recommendations; does not execute or sandbox target skills.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
