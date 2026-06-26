## Description: <br>
飞猪租车智能推荐助手。根据用户出行需求（人数、目的地、时间、品牌偏好）推荐最适合的租车车型，支持调用飞猪租车Mtop API查询实时库存。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maqianqiandegithup](https://clawhub.ai/user/maqianqiandegithup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers use this skill to describe a rental-car trip and receive ranked vehicle recommendations with prices, provider details, and booking links. The agent collects destination, rental dates, passenger count, and optional brand preference, then queries Fliggy/Mtop inventory and presents the top matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trip details such as destination, rental dates, passenger count, and filter preferences may be sent to Fliggy/Mtop to retrieve live inventory and pricing. <br>
Mitigation: Collect only the trip details needed for search, and do not provide account cookies, payment information, identity documents, or unrelated personal data through the skill. <br>
Risk: Vehicle availability and prices are real-time values and may change before checkout. <br>
Mitigation: Confirm the final provider, price, fees, and booking terms on the trusted OTA page before completing a reservation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/maqianqiandegithup/rent-skill) <br>
- [Fliggy rental car OTA page](https://outfliggys.m.taobao.com/app/trip/rx-vehicle-ota/pages/home) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown recommendations with tables, vehicle images or links when available, inline API query examples, and OTA booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are based on live inventory and pricing returned by Fliggy/Mtop and may change before booking.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
