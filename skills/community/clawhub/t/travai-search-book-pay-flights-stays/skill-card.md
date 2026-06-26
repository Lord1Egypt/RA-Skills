## Description: <br>
Search flights and stays, then create card or crypto payments via TravAI. Use when the user asks about flights, travel planning, booking trips, finding accommodation, or travel inspiration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirikov](https://clawhub.ai/user/kirikov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and agent users use this skill to search, compare, price, and book flights or stays through TravAI, including card or crypto payment flows. It is intended for users who explicitly want a TravAI-mediated booking workflow and are ready to confirm itinerary, traveler, cancellation, and payment details before purchase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask the agent to handle account credentials, bearer tokens, passport-matching traveler details, contact information, wallet addresses, and payment information. <br>
Mitigation: Use the skill only for intended TravAI searches or bookings, and provide sensitive information only when comfortable sending it to TravAI. <br>
Risk: Payment creation can start a card checkout or crypto payment flow using user-selected itinerary and traveler data. <br>
Mitigation: Require explicit confirmation of itinerary, traveler details, final price, cancellation terms, payment method, token/network, refund wallet, and each payment creation step. <br>
Risk: Booking changes and cancellations are not handled through the API. <br>
Mitigation: Confirm cancellation terms before payment and direct change or cancellation requests to TravAI support. <br>


## Reference(s): <br>
- [ClawHub TravAI skill page](https://clawhub.ai/kirikov/travai-search-book-pay-flights-stays) <br>
- [Publisher profile](https://clawhub.ai/user/kirikov) <br>
- [TravAI OpenAPI schema](https://api.travai.tech/openapi.json) <br>
- [TravAI API base](https://api.travai.tech) <br>
- [TravAI app profile](https://app.travai.tech/profile) <br>
- [TravAI support Telegram](https://t.me/travaiofficial) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown responses with travel search comparisons, itinerary details, pricing summaries, payment links, exact crypto deposit instructions, and API status messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TravAI account or bearer token for most endpoints and may collect traveler identity details, contact information, wallet addresses, and payment choices during confirmed booking flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
