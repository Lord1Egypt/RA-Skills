## Description: <br>
TravelHound compares live flight and hotel options across major travel platforms, checks booking timing, stacks OTA coupons, and adds destination intelligence for trip planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to compare flights, hotels, coupons, and destination context before deciding when and where to book. It supports flight-only, hotel-only, and combined trip-planning workflows in English or Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad travel-related trigger phrases may invoke the skill during general travel discussions. <br>
Mitigation: Confirm that the user wants travel search or booking guidance before running browser steps or companion-skill commands. <br>
Risk: The skill asks the agent to browse live travel, hotel, coupon, and news sources, so results can change quickly or vary by region, account status, and platform availability. <br>
Mitigation: Show source platform context, note membership or tax assumptions, and ask the user to verify final prices and terms on the booking site before purchase. <br>
Risk: Companion-skill commands for CouponClaw and NewsToday may run additional searches based on trip details. <br>
Mitigation: Review the generated companion-skill commands before execution and avoid sending unnecessary personal travel details. <br>


## Reference(s): <br>
- [TravelHound on ClawHub](https://clawhub.ai/jiajiaoy/travelhound) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [CouponClaw](https://github.com/jiajiaoy/CouponClaw) <br>
- [NewsToday](https://github.com/jiajiaoy/NewsToday) <br>
- [BuyWise](https://github.com/jiajiaoy/BuyWise) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown travel report with comparison tables, booking verdicts, browser research steps, and companion-skill commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include flight and hotel price comparisons, coupon checks, destination news, visa and safety notes, exchange-rate context, and English or Chinese response text.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
