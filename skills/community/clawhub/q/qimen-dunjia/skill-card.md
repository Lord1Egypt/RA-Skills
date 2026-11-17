## Description:

奇门遁甲排盘系统。命令行版本，直接输出盘面解读（财运/事业/感情指数、吉方吉色、秘法推语）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dayou-ht](https://clawhub.ai/user/dayou-ht)

### License/Terms of Use:

MIT-0

## Use Case:

External users run this Node-based Chinese Qimen Dunjia CLI to generate entertainment-focused timing, divination, fortune, relationship, auspicious direction, and auspicious color readings for a selected date and time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HTML interface loads browser dependencies from public CDNs.

Mitigation: Prefer the local Node CLI described in SKILL.md, or pin, integrity-check, or vendor the browser dependencies before using the HTML UI in sensitive contexts.

Risk: The generated divination and fortune guidance could be mistaken for decision-grade advice.

Mitigation: Treat outputs as entertainment and cultural reference only, and use independent information for important personal, financial, or operational decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dayou-ht/skills/qimen-dunjia)
- [Publisher Profile](https://clawhub.ai/user/dayou-ht)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI output with Chinese chart analysis and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts an optional date-time argument; otherwise uses the current local time.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
