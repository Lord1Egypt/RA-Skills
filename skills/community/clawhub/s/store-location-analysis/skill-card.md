## Description: <br>
开店选址分析根据目标地址和业态调用高德地图数据，评估周边设施、交通、人群画像、消费环境和竞品情况，并生成交互式 HTML 选址报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to evaluate whether a proposed address is suitable for a retail, restaurant, or service business. The skill asks for an address, store type, and optional radius, then produces a scored location assessment and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML reports can embed unescaped user-provided or map-provider data, which may allow script injection when the report is opened in a browser. <br>
Mitigation: Open generated reports only from trusted input and trusted provider data, and prefer a version that HTML-escapes displayed fields and safely JSON-encodes data used in scripts. <br>
Risk: Passing the Amap API key as a command-line argument can expose the key through shell history or process listings. <br>
Mitigation: Set AMAP_KEY as an environment variable and avoid putting the key directly on the command line. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/store-location-analysis) <br>
- [高德地图 API 配置指南](references/api_config.md) <br>
- [高德开放平台 Web 服务 Key](https://console.amap.com/dev/key/app) <br>
- [高德地图 Web 服务 API endpoint](https://restapi.amap.com/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, shell commands, JSON analysis data, and an interactive HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AMAP_KEY environment variable or command-line API key; generated reports should be opened only when input and provider data are trusted.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
