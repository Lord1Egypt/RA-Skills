## Description: <br>
Compares flight and train ticket prices across multiple platforms, including real-time 12306 train availability, optional Firecrawl-rendered Ctrip flight data, booking links, mobile quick links, and discount condition details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amurtiger01](https://clawhub.ai/user/amurtiger01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to compare domestic China and international flight or train options, inspect real-time fares or availability where available, and open provider-specific booking links. It is intended for travel price discovery and comparison, not autonomous purchasing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route, date, and city searches may be shared with 12306, Ctrip, Firecrawl, Tequila, or Amadeus depending on configuration. <br>
Mitigation: Only configure optional provider API keys for services the user accepts, and avoid submitting sensitive travel searches unless external provider disclosure is acceptable. <br>
Risk: Optional API keys and client secrets are sensitive credentials. <br>
Mitigation: Store provider credentials in environment variables and limit them to the services needed for the search. <br>
Risk: Ticket prices, availability, booking links, and discount conditions can change before purchase. <br>
Mitigation: Verify prices, seat availability, refund rules, baggage terms, and eligibility conditions on the booking platform before buying. <br>


## Reference(s): <br>
- [Ticket Price Compare on ClawHub](https://clawhub.ai/amurtiger01/ticket-price-compare) <br>
- [Ticket Price Comparison Platform Detailed Guide](references/platforms_guide.md) <br>
- [Firecrawl](https://firecrawl.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text with fare tables, route summaries, provider links, discount notes, and optional bash commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include real-time external query results, direct booking or search links, and warnings when live flight data is unavailable.] <br>

## Skill Version(s): <br>
1.2.6 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
