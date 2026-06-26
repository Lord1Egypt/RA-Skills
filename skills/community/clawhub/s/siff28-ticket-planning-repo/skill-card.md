## Description: <br>
用于根据任意影片清单与偏好规划 SIFF 2026 买票和观影行程；优先使用内置官方排片数据，并评估片长、散场缓冲、跨影院驾车时间与备选场次。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fffonion](https://clawhub.ai/user/fffonion) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External moviegoers and festival planners use this skill to turn film wishlists, date preferences, and approximate anchor points into SIFF 2026 ticket-buying priorities, daily viewing itineraries, transfer-risk notes, and optional export files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Planning quality can depend on approximate personal anchor points such as home, work, or preferred rest locations. <br>
Mitigation: Use rough landmarks instead of exact private addresses and keep anchor labels anonymous in any generated itinerary or export. <br>
Risk: Bundled driving and metro travel times are estimates and may not reflect live traffic, crowding, last-train timing, weather, or parking delays. <br>
Mitigation: Verify risky transfers, late-night return plans, and tight buffers against current transport information before buying tickets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fffonion/siff28-ticket-planning-repo) <br>
- [SIFF 2026 Schedule Page](https://www.siff.com/page/paipian) <br>
- [SIFF 2026 Official Schedule JSON](https://www.siff.com/files/2026/cndata-20260603-001.json) <br>
- [SIFF 2026 Official Schedule Export](https://www.siff.com/schedule/paipianexportcn) <br>
- [SIFF 2026 Yangtze Delta Screenings](https://www.siff.com/content?aid=101260602141949831498906159288325659) <br>
- [MetroFlow Shanghai Metro Data](https://figshare.com/collections/ARIZONA_Sun/4209384) <br>
- [MetroFlow Station Info Source](https://raw.githubusercontent.com/Ariza-Sun/MetroFlow/main/Data/stationInfo.csv) <br>
- [Embedded SIFF 2026 Reference Manifest](references/siff2026/manifest.json) <br>
- [Embedded SIFF 2026 Scrape Summary](references/siff2026/siff2026-scrape-summary.json) <br>
- [Embedded SIFF 2026 Cinema Routing Manifest](references/siff2026/siff2026-cinema-routing-manifest.json) <br>
- [Embedded SIFF 2026 Metro Routing Manifest](references/siff2026/siff2026-cinema-metro-routing-manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with itinerary tables, ticket-buying priorities, risk notes, and optional CSV or iCal exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include estimated travel times, anonymous anchor-point labels, fallback screenings, and export-ready schedule data.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter states 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
