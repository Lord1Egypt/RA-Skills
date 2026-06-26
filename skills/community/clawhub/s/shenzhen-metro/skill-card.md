## Description: <br>
Helps agents answer Shenzhen Metro questions about lines, stations, fares, schedules, transfers, passenger flow, nearby amenities, discounts, accessibility, and points of interest using unofficial reference data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mickey406](https://clawhub.ai/user/mickey406) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to answer Shenzhen Metro trip-planning and station-information questions, including route, fare, schedule, transfer, crowding, amenity, and nearby-place lookups. <br>

### Deployment Geography for Use: <br>
Global; content is specific to Shenzhen, China. <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses unofficial, unverified Shenzhen Metro reference data that may be wrong or stale for schedules, fares, emergencies, or service changes. <br>
Mitigation: Verify important travel, fare, emergency, and schedule details with Shenzhen Metro official sources before relying on the answer. <br>
Risk: Optional Amap API use requires adding a user API key to the local data file. <br>
Mitigation: Use a restricted Amap key and do not publish or share an edited data file containing a real key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mickey406/shenzhen-metro) <br>
- [Publisher profile](https://clawhub.ai/user/mickey406) <br>
- [Amap Place Text API example](https://restapi.amap.com/v3/place/text?city=深圳&keywords=车公庙站&key=YOUR_API_KEY) <br>
- [Shenzhen Metro official site](https://www.szmc.net) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, API Calls, configuration] <br>
**Output Format:** [Markdown or plain text answers with optional shell command examples for Amap API calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may cite offline JSON facts or optional external Amap/TTS calls when configured by the user.] <br>

## Skill Version(s): <br>
3.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
