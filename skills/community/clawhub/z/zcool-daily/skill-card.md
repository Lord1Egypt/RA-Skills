## Description: <br>
自动获取站酷（ZCOOL）首页热门设计作品（带链接、分类、亮点描述、趋势统计）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heihu123](https://clawhub.ai/user/heihu123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, content editors, and developers use this skill to fetch ZCOOL homepage work links and produce a daily Markdown-style recommendation digest with categories, highlights, and trend counts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawHub security evidence marks the bundle suspicious and says it is intended for trusted maintainer use. <br>
Mitigation: Install only in a trusted ClawHub maintainer environment and review the security guidance before use. <br>
Risk: Security guidance warns that helper defaults may grant broad local access when nested automation is used. <br>
Mitigation: Review execution defaults and prefer restricted options unless full local access is intentional. <br>
Risk: Security guidance warns that staff moderation workflows can make production changes. <br>
Mitigation: Do not use moderation workflows unless the operator has legitimate staff authority and understands the production impact. <br>


## Reference(s): <br>
- [Output example](references/output-example.md) <br>
- [ZCOOL homepage](https://www.zcool.com.cn/) <br>
- [ClawHub skill page](https://clawhub.ai/heihu123/zcool-daily) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style text digest saved as a dated .txt file and printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches up to 10 ZCOOL work entries, classifies them by design category, adds short highlight text, and writes zcool_daily/zcool_{date}.txt.] <br>

## Skill Version(s): <br>
1.0.7 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
