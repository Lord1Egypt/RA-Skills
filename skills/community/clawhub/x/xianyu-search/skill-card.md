## Description:

Generates second-hand marketplace search links and Markdown recommendation reports for Xianyu, Zhuanzhuan, and Paipai based on budget, condition, battery, location, and seller-credit criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lg2021888](https://clawhub.ai/user/lg2021888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn natural-language second-hand shopping requests into marketplace search links, comparison tables, recommendations, inspection checklists, and transaction-safety guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags unsafe MDM-bypass purchase wording.

Mitigation: Reject listings described as enterprise MDM, managed, activation-locked, bypassed, or not fully de-enrolled by the legitimate owner or organization.

Risk: The security evidence flags an unpinned npx clawhub@latest install command.

Mitigation: Verify the ClawHub CLI package identity and prefer a pinned scoped installer before installation.

Risk: The skill generates marketplace links and recommendation text rather than verified real-time listings.

Mitigation: Open marketplace links directly and verify price, condition, seller identity, device locks, and transaction terms before making a purchase decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lg2021888/skills/xianyu-search)
- [Xianyu / Goofish](https://www.goofish.com)
- [Zhuanzhuan](https://www.zhuanzhuan.com)
- [Paipai](https://www.paipai.com)
- [Yanhuobao inspection service](https://www.yanhuobao.com)
- [12315 consumer complaint portal](https://www.12315.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports, marketplace URLs, checklist text, bargaining scripts, and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill generates links and recommendations from user input; it does not directly scrape marketplace listings or execute external API calls.]

## Skill Version(s):

1.0.2 (source: server release evidence, package.json, clawhub.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
