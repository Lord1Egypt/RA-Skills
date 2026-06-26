## Description: <br>
小鹿选房是专业的涵盖全国的房产信息平台，当用户需要找房源（二手房、租房、新房、买房、找房）、选笋盘、比价格、查成交、看小区、查学区、查学校时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangjike](https://clawhub.ai/user/fangjike) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External home seekers and real-estate users use this skill to search supported Chinese cities for second-hand homes, rentals, new homes, communities, schools, and transaction prices through the xiaolu-house CLI. <br>

### Deployment Geography for Use: <br>
China (supported cities listed by the skill) <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs the xiaolu-house npm CLI and requires an API key for the housing service. <br>
Mitigation: Install only if the publisher and package are trusted, review the source or package when needed, and confirm before setting or clearing local configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fangjike/xiaolu-house) <br>
- [xiaolu-house homepage](https://github.com/fanggeek/xiaolu-house) <br>
- [API key setup page](https://www.xiaoluxuanfang.com/claw) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and natural-language summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the xiaolu-house npm CLI, may store an API key/config locally, and should observe the documented one-request-per-second rate limit.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
