## Description: <br>
Converts chart requests and structured CSV or JSON data into ECharts chart configurations, HTML previews, and optional SVG or PNG exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ifeel-is-a-mouse](https://clawhub.ai/user/ifeel-is-a-mouse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn chart requests or CSV/JSON data into ECharts visualizations for reports, previews, and local export workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML is executable content. <br>
Mitigation: Open generated HTML only from trusted data and review chart options before sharing or publishing. <br>
Risk: CDN-based chart output can fail offline or depend on external script loading. <br>
Mitigation: Use --embed when offline or reproducible output is needed. <br>
Risk: SVG or PNG export may use Playwright and temporary files. <br>
Mitigation: Run export workflows in a trusted local workspace and review generated files before reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ifeel-is-a-mouse/text2echart) <br>
- [Apache ECharts option documentation](https://echarts.apache.org/en/option.html) <br>
- [ECharts wordcloud documentation](https://ecomfe.github.io/echarts-wordcloud/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with HTML, JSON, and shell command snippets; CLI workflows may produce HTML, SVG, or PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [SVG and PNG export paths may use Playwright; --embed can create offline HTML output.] <br>

## Skill Version(s): <br>
2.3.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
