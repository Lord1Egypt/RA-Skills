## Description: <br>
AI-powered supply chain and logistics intelligence skill that tracks freight rates, port throughput, trade flows, transit times, equipment availability, commodity bottlenecks, and logistics risk factors to produce disruption alerts and cost optimization insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze global supply chain disruptions, freight costs, port congestion, trade flows, commodity bottlenecks, and sourcing risks. It helps generate dashboards, disruption assessments, scenario comparisons, and operational recommendations from cited logistics data sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Supply chain data can become stale quickly and may affect operational recommendations. <br>
Mitigation: Verify data vintage and source URLs before acting, and flag information older than seven days. <br>
Risk: Some listed data sources may require separate access, licensing, or permission. <br>
Mitigation: Confirm source permissions and licensing before using proprietary or restricted data in workflows. <br>
Risk: Broad business triggers may activate the skill for adjacent logistics questions. <br>
Mitigation: Confirm the requested geography, logistics mode, commodity, and time horizon before generating recommendations. <br>


## Reference(s): <br>
- [Supply Chain Data Sources](references/supply_chain_sources.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/ai-gaoqian/supply-chain-intel) <br>
- [Drewry Container Freight Index](https://www.drewry.co.uk/supply-chain-advisors/supply-chain-expertise/world-container-index-assessed-by-drewry) <br>
- [Freightos Baltic Index](https://fbx.freightos.com/) <br>
- [UN Comtrade Database](https://comtradeplus.un.org/) <br>
- [US Census Bureau Trade Data](https://www.census.gov/foreign-trade/statistics/) <br>
- [Flexport Ocean Timeliness Indicator](https://www.flexport.com/oti/) <br>
- [World Bank Logistics Performance Index](https://lpi.worldbank.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown tables and concise narrative analysis with cited source URLs, data vintage, confidence notes, and scenario recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include freight snapshots, port congestion dashboards, commodity bottleneck matrices, risk heatmaps, cost benchmarks, and disruption alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
