## Description: <br>
Agent travel middleware for searching flights, hotels, and car rentals, assembling policy-aware itineraries, managing traveler preferences, and preparing payment-ready booking workflows via Stripe Checkout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robinmtzieme-commits](https://clawhub.ai/user/robinmtzieme-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and travel workflow agents use Zim to search and compare flights, hotels, and car rentals, assemble policy-aware itineraries, manage traveler preferences and approvals, and prepare Stripe Checkout payment flows. It is suited to booking-ready recommendations and payment orchestration, while supplier reservations remain manual or placeholder unless a real executor is added. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment and booking workflows can expose high-impact operational data and may be mistaken for completed supplier reservations. <br>
Mitigation: Use Stripe test keys first, clearly distinguish payment collection from supplier-side reservation execution, and do not present trips as fully booked without provider confirmation. <br>
Risk: Traveler PII, conversations, approvals, booking records, and webhook payloads may persist locally or flow through third-party services. <br>
Mitigation: Set ZIM_API_KEY and a separate ZIM_ADMIN_KEY, require Stripe and Twilio webhook secrets, restrict database file permissions, avoid storing real passport data unless necessary, and define retention and deletion rules. <br>
Risk: Search and booking flows rely on affiliate APIs, Stripe, Twilio, SerpApi, OpenRouter, and outbound travel links that require sensitive credentials and user disclosure. <br>
Mitigation: Disclose affiliate links and third-party AI/provider processing to users, scope environment credentials tightly, and review all configured provider accounts before live deployment. <br>


## Reference(s): <br>
- [ClawHub Zim release page](https://clawhub.ai/robinmtzieme-commits/zim) <br>
- [Publisher profile](https://clawhub.ai/user/robinmtzieme-commits) <br>
- [API guide](references/api-guide.md) <br>
- [Agent-to-agent booking guide](references/agent-to-agent-booking.md) <br>
- [Travelpayouts support](https://support.travelpayouts.com/hc/en-us/categories/200358578) <br>
- [Travelpayouts prices API](https://api.travelpayouts.com/aviasales/v3/prices_for_dates) <br>
- [Booking.com hotel search](https://www.booking.com/searchresults.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON responses, CLI output, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include affiliate deeplinks, booking-ready summaries, approval states, Stripe Checkout session status, and WhatsApp response text.] <br>

## Skill Version(s): <br>
3.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
