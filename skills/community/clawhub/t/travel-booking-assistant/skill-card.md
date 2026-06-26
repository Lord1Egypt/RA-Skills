## Description: <br>
Booking.com international hotel booking assistant for global hotel search, room availability, price comparison, and reservation-management workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel agents, assistants, and end users can use this skill to search international hotels, inspect room options, compare prices and cancellation terms, and manage Booking.com-style reservations. Reviewers should treat booking and cancellation flows cautiously because the security evidence says the release appears unfinished and may present fake prices or terms as Booking.com results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the release appears unfinished and may show fake hotel prices or cancellation terms as Booking.com results. <br>
Mitigation: Use only after replacing mock responses with verified Booking.com API responses and clearly labeling any non-live or sample data. <br>
Risk: Booking and cancellation actions can affect real travel plans or payments if connected to production APIs. <br>
Mitigation: Require explicit user confirmation before creating or cancelling reservations and display authoritative price, tax, fee, and cancellation-policy details from the live provider. <br>
Risk: Network and credential handling are not documented in the release evidence. <br>
Mitigation: Document required API credentials, storage expectations, network endpoints, and operational limits before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-zry/travel-booking-assistant) <br>
- [Booking.com Affiliate API endpoint referenced by the skill](https://distribution-xml.booking.com/json/bookings.getHotels) <br>
- [Booking.com distribution XML JSON base URL referenced by the artifact](https://distribution-xml.booking.com/json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses, JSON-like API payloads, Python function-call schemas, and formatted hotel or room tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Booking.com API credentials before real API-backed use.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata, release evidence, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
