## Description: <br>
专为实体商业打造的 AI 选址洞察专家。通过动态商业战略追问与高德 LBS 数据引擎，全自动生成包含「竞品雷达」、「客流推演」与「多维横评矩阵」的交互式可视化研报，让开店决策更科学。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzhyjr2021-beep](https://clawhub.ai/user/hzhyjr2021-beep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business operators and commercial analysts use this skill to gather required site-selection strategy inputs, fetch candidate location coordinates, and generate a comparative business location report for physical retail decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends business and location details to external mapping and search services. <br>
Mitigation: Run it only with user approval for those external services and avoid submitting confidential business plans unless disclosure is acceptable. <br>
Risk: Generated HTML reports may expose sensitive business details and can include the AMap key in map URLs. <br>
Mitigation: Store reports in a controlled directory, remove API keys from shared outputs, and review the report before distribution. <br>
Risk: Local report and temporary state writes use weak safeguards. <br>
Mitigation: Use an explicit output directory, sanitized filenames, and appropriate local file permissions before operational use. <br>
Risk: Rate-limit-evasion language appears in the security summary and artifact behavior. <br>
Mitigation: Use compliant API quota handling and avoid behavior intended to bypass provider limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hzhyjr2021-beep/smart-site-selection-skill) <br>
- [Publisher profile](https://clawhub.ai/user/hzhyjr2021-beep) <br>
- [AMap Open Platform](https://console.amap.com) <br>
- [AMap Around Search API](https://restapi.amap.com/v3/place/around) <br>
- [AMap Static Map API](https://restapi.amap.com/v3/staticmap) <br>
- [ECharts CDN dependency](https://cdn.staticfile.net/echarts/5.5.0/echarts.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, shell commands, code, configuration, files] <br>
**Output Format:** [Conversational guidance plus a generated single-file HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMAP_WEBSERVICE_KEY and may write local report files and temporary state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter; package.json reports 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
