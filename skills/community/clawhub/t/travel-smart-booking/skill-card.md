## Description: <br>
A hotel aggregation skill that helps agents structure searches across Fenbeitong, Ctrip, Meituan, Tongcheng, Huazhu, and Jinjiang and present normalized hotel, room, price, and booking-source information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, travel assistants, and developers use this skill to organize multi-platform hotel searches, compare available prices by source, and format hotel aggregation results for review before booking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary says the skill is incomplete and overstates real hotel search and booking capability. <br>
Mitigation: Treat it as a prototype until real provider integrations are added and verified; do not rely on it for prices, availability, room details, or reservations. <br>
Risk: Travel booking can expose personal, itinerary, and payment-related information. <br>
Mitigation: Add privacy disclosure, minimize collected user data, and require explicit confirmation before any booking or reservation action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-zry/travel-smart-booking) <br>
- [Fenbeitong Open API endpoint](https://openapiv2.fenbeitong.com) <br>
- [Ctrip API endpoint](https://api.ctrip.com) <br>
- [Meituan API endpoint](https://api.meituan.com) <br>
- [Tongcheng API endpoint](https://api.tongcheng.com) <br>
- [Huazhu API endpoint](https://api.huazhu.com) <br>
- [Jinjiang API endpoint](https://api.jinjiang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, API Calls, Guidance] <br>
**Output Format:** [JSON responses and Markdown tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; hotel search and booking results must come from real provider integrations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
