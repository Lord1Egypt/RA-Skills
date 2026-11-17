## Description:

A China social-security and housing-fund assistant that provides local contribution calculations, pension estimates, simulated query outputs, and official-channel lookup guidance for major cities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[testmtcode](https://clawhub.ai/user/testmtcode)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to estimate social-security, housing-fund, payroll contribution, and pension figures for selected Chinese cities and to find official channels for real account lookup.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill accepts sensitive identifiers such as ID-card numbers and housing-fund account numbers in command-line arguments.

Mitigation: Use non-sensitive test values for simulations and enter real identifiers only through verified official services.

Risk: Some official-service links in the skill use plain HTTP.

Mitigation: Manually verify the destination and use HTTPS before logging in or entering any credentials, verification codes, or personal data.

Risk: Account lookup outputs are simulated and contribution rates may change over time.

Mitigation: Treat generated values as estimates or guidance and confirm real balances, eligibility, and final amounts with official local agencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/testmtcode/skills/social-security-fund)
- [Publisher profile](https://clawhub.ai/user/testmtcode)
- [Artifact README](artifact/README.md)
- [Skill source file](artifact/SKILL.md)
- [Beijing Human Resources and Social Security Bureau](http://rsj.beijing.gov.cn/)
- [Beijing Housing Fund](http://gjj.beijing.gov.cn/)
- [Shanghai Human Resources and Social Security Bureau](http://rsj.sh.gov.cn/)
- [Shanghai Housing Fund](http://www.shgjj.com/)
- [Guangzhou Human Resources and Social Security Bureau](http://rsj.gz.gov.cn/)
- [Guangzhou Housing Fund](http://gjj.gz.gov.cn/)
- [Shenzhen Social Insurance Fund Administration](http://hrss.sz.gov.cn/szsi/)
- [Shenzhen Housing Fund](http://zjj.sz.gov.cn/)
- [Hangzhou Human Resources and Social Security Bureau](http://hrss.hangzhou.gov.cn/)
- [Hangzhou Housing Fund](http://gjj.hangzhou.gov.cn/)
- [Chengdu Human Resources and Social Security Bureau](http://cdhrss.chengdu.gov.cn/)
- [Chengdu Housing Fund](http://gjj.chengdu.gov.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown-style terminal text or JSON from Python command-line tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include calculated contribution and pension estimates, simulated account-style summaries, and official lookup-channel guidance.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
