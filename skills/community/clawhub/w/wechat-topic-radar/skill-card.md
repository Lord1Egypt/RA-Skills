## Description: <br>
聚合多平台热点，智能评估选题潜力，提供爆款切入角度、竞品分析及差异化内容方案，助力公众号内容创作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sxzxlj](https://clawhub.ai/user/sxzxlj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, new media operators, and developers use this skill to scan hot topics across Chinese social, news, and technology platforms, score topic potential, compare angles, and generate content planning reports for WeChat public accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts third-party trend APIs and platforms during topic collection. <br>
Mitigation: Install and run it only in environments where network collection from those platforms is acceptable, and review platform API or scraping terms before use. <br>
Risk: Generated HTML reports may load remote Plotly assets. <br>
Mitigation: Open generated reports only when remote asset loading is acceptable, or adapt the report generation path for offline assets in stricter environments. <br>
Risk: Exported topic data and reports may contain third-party content or trend data that should not be shared broadly. <br>
Mitigation: Review generated JSON and HTML reports before distribution, especially when they include platform-derived topics, URLs, or engagement data. <br>
Risk: Dependency and network behavior can vary across Python environments. <br>
Mitigation: Pin dependencies, use a controlled Python environment, and keep HTTPS-only sources where possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sxzxlj/wechat-topic-radar) <br>
- [Publisher profile](https://clawhub.ai/user/sxzxlj) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Configuration](artifact/config/config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, HTML files] <br>
**Output Format:** [Console text, Python API results, JSON exports, and generated HTML reports with visual charts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports may include trend rankings, heat scores, keywords, topic analyses, title suggestions, content outlines, and competitor differentiation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, target metadata, and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
