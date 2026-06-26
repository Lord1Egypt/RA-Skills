## Description: <br>
Find and monitor estimated gas prices within a US radius, focusing on Costco discounts and daily alerts for selected fuel types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GustavoZiaugra](https://clawhub.ai/user/GustavoZiaugra) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Drivers and agent operators use this skill to search nearby fuel stations by ZIP code or coordinates, compare estimated prices, and schedule recurring gas price summaries. It is especially useful for Costco-focused searches and commute or trip planning within the United States. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: ZIP code or coordinate searches may be shared with external services such as OpenStreetMap, Nominatim, Overpass, GasBuddy, or Telegram. <br>
Mitigation: Use only locations you are comfortable sending to those services, and avoid enabling notifications that reveal sensitive travel patterns. <br>
Risk: Gas prices may be estimates or stale, especially outside the documented Columbus, Ohio examples. <br>
Mitigation: Treat results as planning guidance and verify prices with a station, GasBuddy, or another current source before relying on them. <br>
Risk: Daily cron alerts can run recurring network lookups and send recurring notifications. <br>
Mitigation: Enable scheduled alerts intentionally, review the configured ZIP code, radius, fuel type, timezone, and notification target, and disable the schedule when no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/GustavoZiaugra/test-gas-skill) <br>
- [US city coordinates](references/locations.md) <br>
- [Columbus ZIP code reference](references/zip_codes.md) <br>
- [OpenStreetMap Overpass API](http://overpass-api.de/api/interpreter) <br>
- [GasBuddy](https://www.gasbuddy.com) <br>
- [Costco warehouse locator](https://www.costco.com/warehouse-locations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, JSON station records, shell commands, and cron configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write gas price results to a JSON file and may call external location or fuel-price services during use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
