## Description:

飞猪租车智能推荐助手根据用户的目的地、出行时间、人数和品牌偏好推荐适合的飞猪租车车型，并可查询实时库存。

This skill is ready for commercial/non-commercial use.

## Publisher:

[maqianqiandegithup](https://clawhub.ai/user/maqianqiandegithup)

### License/Terms of Use:

MIT-0

## Use Case:

Travel shoppers and agents use this skill to collect rental-car trip requirements, query Fliggy rental-car availability, and present a concise shortlist of suitable vehicles with prices and booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trip details such as city, dates, passenger count, and filters may be sent to Fliggy/Taobao APIs.

Mitigation: Share only the trip details needed for the rental search and review the platform's privacy and booking terms before proceeding.

Risk: Rental prices, inventory, fees, and booking terms can change before purchase.

Mitigation: Confirm the final price, availability, cancellation policy, and rental terms on the official booking page before buying.

Risk: The skill may generate OTA booking links from API response data.

Mitigation: Check that booking links open the expected Fliggy/Taobao destination and verify vehicle and merchant details before entering payment information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maqianqiandegithup/skills/rent-skill)
- [Fliggy rental-car OTA page](https://outfliggys.m.taobao.com/app/trip/rx-vehicle-ota/pages/home)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Chinese-language Markdown recommendations with vehicle details, prices, images, and booking links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Fliggy/Taobao OTA booking links and rental-car query parameters.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
