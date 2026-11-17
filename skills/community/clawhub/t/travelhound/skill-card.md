## Description:

TravelHound compares flights and hotels across Google Flights, Skyscanner, Kayak, Booking.com, Agoda, and Trip.com with book-now-vs-wait timing, OTA coupon stacking, and destination intelligence for visa, FX trend, and safety checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use TravelHound to compare flight and hotel options, check coupon opportunities, and assemble destination-aware trip guidance. It supports book-now-vs-wait decisions by prompting the agent to gather current prices, price forecasts, safety advisories, exchange-rate context, and destination news.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary flags an unrelated promotional star request appended to useful replies.

Mitigation: Review generated replies before use and remove maintainer-promotion text from user-facing travel answers.

Risk: The skill sends travel details to external travel, search, coupon, and news services while gathering current prices and destination context.

Mitigation: Avoid entering sensitive personal travel details unless the user accepts those external service interactions.

Risk: The skill prompts agents to rely on live third-party prices, forecasts, advisories, and coupon information that may change quickly.

Mitigation: Verify important fare, hotel, visa, safety, and coupon details directly with authoritative or booking sources before acting.

## Reference(s):

- [TravelHound on ClawHub](https://clawhub.ai/jiajiaoy/skills/travelhound)
- [OpenClaw](https://openclaw.ai)
- [CouponClaw](https://github.com/jiajiaoy/CouponClaw)
- [NewsToday](https://github.com/jiajiaoy/NewsToday)
- [BuyWise](https://github.com/jiajiaoy/BuyWise)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style travel comparison reports with browser, web search, and OpenClaw command instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include travel platform links, coupon lookup commands, price comparison tables, budget estimates, and booking recommendations.]

## Skill Version(s):

1.1.5 (source: package.json, release metadata, and version footer)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
