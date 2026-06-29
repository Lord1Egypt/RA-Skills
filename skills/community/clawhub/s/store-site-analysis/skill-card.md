## Description: <br>
基于高德开放平台，为 AI Agent 提供单地址商铺选址分析和多地址对比评估，生成 POI、交通、评分和地图可视化结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wukongmazi](https://clawhub.ai/user/wukongmazi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators, analysts, and AI agents use this skill to evaluate prospective store locations, compare two to five candidate addresses, and produce reviewable site-selection evidence from nearby competitors, facilities, traffic status, weighted scores, and map visualizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Address and location queries are sent to AMap services for geocoding, POI lookup, reverse geocoding, and traffic status. <br>
Mitigation: Use the skill only for locations you are comfortable sharing with AMap, and avoid submitting sensitive or confidential addresses unless that disclosure is acceptable. <br>
Risk: Generated HTML reports can contain addresses, coordinates, nearby businesses and facilities, and an AMap JS key. <br>
Mitigation: Store generated reports in a private directory, avoid broadly sharing them, and delete them after use when the location data or key exposure is no longer needed. <br>
Risk: Site-selection recommendations rely on external POI and traffic data plus a fixed weighted scoring method. <br>
Mitigation: Treat the output as decision-support evidence and verify important business, lease, foot-traffic, and regulatory assumptions before acting on a store-location decision. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wukongmazi/store-site-analysis) <br>
- [AMap Open Platform API Documentation](https://lbs.amap.com/api/) <br>
- [AMap Open Platform](https://lbs.amap.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [JSON responses with generated HTML visualization file paths and human-facing analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-address mode returns location, competitor, facility, traffic, and heatmap details; compare mode returns ranked candidate locations, component scores, a recommendation, and a comparison HTML path.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
