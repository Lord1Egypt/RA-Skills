## Description: <br>
用于微博创作者数据、微博用户资料、账号资料、创作者画像、主页信息和粉丝规模查询。覆盖 Weibo creator profiles，来自 SocialDataX 社媒数据助手。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devinchen2014](https://clawhub.ai/user/devinchen2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to perform read-only SocialDataX lookups for Weibo creator profile details, including account basics, profile fields, verification, audience size, and related public creator information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes an external npm package at latest, so package behavior can change after publication. <br>
Mitigation: Install only when SocialDataX is trusted, review package behavior before use, and pin or audit the package in controlled environments where repeatability matters. <br>
Risk: The CLI requires SOCIALDATAX_API_KEY, giving the package access to that credential during lookup. <br>
Mitigation: Use a scoped SocialDataX API key where available, provide only the required environment variable, and rotate the key if exposure is suspected. <br>


## Reference(s): <br>
- [SocialDataX homepage and API access](https://socialdatax.com/?from=clawhub) <br>
- [ClawHub skill listing](https://clawhub.ai/devinchen2014/skills/socialdatax-weibo-creator-profile) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON API output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOCIALDATAX_API_KEY, node, and npm; CLI examples use socialdatax-skills@latest.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
